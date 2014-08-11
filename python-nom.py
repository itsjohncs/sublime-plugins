import sublime, sublime_plugin
import subprocess

PYTHON = "/usr/local/bin/python"

class RunPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = sublime.active_window()

        view = window.active_view()
        contents = view.substr(sublime.Region(0, view.size()))

        p = subprocess.Popen([PYTHON], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, universal_newlines=True)

        output = "<murdered>"
        try:
            output = p.communicate(contents, timeout=4)[0]
        except subprocess.TimeoutExpired:
            p.kill()

        panel = window.create_output_panel("pythonom")
        panel.set_read_only(False)
        panel.set_scratch(True)
        panel.settings().set("word_wrap", True)
        panel.run_command("append", {"characters": output})
        window.run_command("show_panel", {"panel": "output.pythonom"})
        panel.set_read_only(True)

