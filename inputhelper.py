import sublime
import sublime_plugin
import subprocess
import os
from stat import *

st_version = 2
if not sublime.version() or int(sublime.version()) > 3000:
    st_version = 3
    u = str
    set_timeout_async = sublime.set_timeout_async
else:
    u = unicode

    import threading
    class Async(threading.Thread):
        def __init__(self, callback):
            self.callback = callback
            threading.Thread.__init__(self)
        def run(self):
            self.callback()

    def set_timeout_async(callback, delay_ms = 0):
        sublime.set_timeout(lambda: Async(callback).start(), delay_ms)

dbname = 'skdb'
binname = 'linux_text_input_gui.py'
usrbin = os.path.join('User', 'InputHelper', 'bin')

def update_binary():
    pkgpath = os.path.join(sublime.installed_packages_path(), 'InputHelper.sublime-package')
    srcdir = os.path.join(sublime.packages_path(), 'InputHelper', 'lib')
    srcpath = os.path.join(srcdir, binname)
    srcdb = os.path.join(srcdir, dbname)
    bindir = os.path.join(sublime.packages_path(), usrbin)
    binpath = os.path.join(bindir, binname)
    bindb = os.path.join(bindir, dbname)
    resdir = 'Packages/InputHelper/lib/'
    resbin = resdir + binname
    resdb = resdir + dbname

    bininfo = None
    bindata = None
    dbdata = None

    if os.path.exists(binpath):
        bininfo = os.stat(binpath)
    elif not os.path.exists(bindir):
        os.makedirs(bindir, 0o755)

    if not os.path.exists(bindb):
        if os.path.exists(srcdb):
            with open(srcdb, 'rb') as srcfile:
                dbdata = srcfile.read()
                srcfile.close
        elif st_version == 3 and os.path.exists(pkgpath):
            dbdata = sublime.load_binary_resource(resdb)
        if dbdata != None:
            print("* Creating " + bindb)
            with open(bindb, 'wb') as dbfile:
                dbfile.write(dbdata)
                dbfile.close()

    if os.path.exists(srcpath):
        srcinfo = os.stat(srcpath)
        if bininfo == None or bininfo[ST_MTIME] < srcinfo[ST_MTIME]:
            with open(srcpath, 'rb') as srcfile:
                bindata = srcfile.read()
                srcfile.close()
    elif st_version == 3 and os.path.exists(pkgpath):
        pkginfo = os.stat(pkgpath)
        if bininfo == None or bininfo[ST_MTIME] < pkginfo[ST_MTIME]:
            bindata = sublime.load_binary_resource(resbin)

    if bindata != None:
        print("* Updating " + binpath)
        with open(binpath, 'wb') as binfile:
            binfile.write(bindata)
            binfile.close()

    if not os.access(binpath, os.X_OK):
        os.chmod(binpath, 0o755)


class InputHelperCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        selected = None
        text_output = None
        args = []
        if len(sel) > 0:
            selected = sel

        if sublime.platform() == 'linux':
            args = [os.path.join(sublime.packages_path(), usrbin, binname)]
            proc = subprocess.Popen(args, stdout=subprocess.PIPE)
            text_output = u(proc.communicate()[0].strip(),'utf-8')
        if text_output:
            for region in sel:
                self.view.replace(edit, region, text_output)


def plugin_loaded():
    if sublime.platform() == 'linux':
        set_timeout_async(update_binary)

if st_version == 2:
    plugin_loaded()
