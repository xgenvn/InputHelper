import sublime
import sublime_plugin
import subprocess
import os

class InputHelperCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        selected = None
        text_output = None
        args = []
        if len(sel) > 0:
            selected = sel

        if sublime.platform() == 'linux':

            location = os.path.join(sublime.packages_path(), 'InputHelper', 'lib', 'linux_text_input_gui.py')
            args = [location]

            if not os.access(location, os.X_OK):
                os.chmod(location, 0755)

            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            text_output = unicode(proc.communicate()[0].strip(),'utf-8')
        if text_output:
            for region in sel:
                self.view.replace(edit, region, text_output)