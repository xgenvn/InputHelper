#!/usr/bin/env python
import pygtk

pygtk.require('2.0')
import gtk

class SimpleTextInput:
    def print_text(self):
        buffer = self.textInput.get_buffer()
        print(buffer.get_text())

    def destroy(self, widget, data=None):
        if self.print_text_flag == False:
            self.print_text()
        gtk.main_quit()

    def on_key_press(self, widget, event):
        keyname = gtk.gdk.keyval_name(event.keyval)
        if event.state & gtk.gdk.CONTROL_MASK and keyname == 'Return' or keyname == 'Return':
            self.print_text()
            self.print_text_flag = True
            self.destroy(self, widget)
        if keyname == 'Escape':
            gtk.main_quit()

    def __init__(self):
        # create a new window
        self.print_text_flag = False
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title("Input Helper")
        window.set_default_size(300, 60)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.connect("destroy", self.destroy)
        window.set_border_width(10)
        self.textInput = gtk.Entry()
        self.textInput.set_tooltip_text("Press Ctrl-Enter or Enter to insert string")
        self.textInput.connect("key_press_event", self.on_key_press)
        window.add(self.textInput)
        window.show_all()

    def main(self):
        gtk.main()


if __name__ == "__main__":
    txt = SimpleTextInput()
    txt.main()
