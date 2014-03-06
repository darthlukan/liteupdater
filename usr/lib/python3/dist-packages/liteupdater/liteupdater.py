#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from gi.repository import Gtk


class SystrayApp(object):

    def __init__(self):
        self.tray = Gtk.StatusIcon()

        if os.path.isfile('/usr/share/pixmaps/updaten.png'):
            self.tray.set_from_file('/usr/share/pixmaps/updaten.png')
        else:
            self.tray.set_from_stock(Gtk.STOCK_ABOUT)

        self.tray.set_tooltip_text('Lite Updater')
        self.tray.connect('popup-menu', self.on_right_click)

    def on_right_click(self, icon, event_button, event_time):
        print("Right-click fired")
        self.make_menu(icon, event_button, event_time)

    def make_menu(self, icon, event_button, event_time):
        self.menu = Gtk.Menu()

        about = Gtk.MenuItem()
        about.set_label("About")
        about.connect('activate', self.show_about_dialog)

        quit_action = Gtk.MenuItem()
        quit_action.set_label("Quit")
        quit_action.connect("activate", Gtk.main_quit)

        self.menu.append(about)
        self.menu.append(quit_action)

        self.menu.show_all()

        def pos(menu, icon):
            return Gtk.StatusIcon.position_menu(menu, icon)

        self.menu.popup(None, None, pos, icon, event_button, event_time)
        print("Menu should have popped up")

    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name('Lite Updater')
        about_dialog.set_name('Lite Updater')
        about_dialog.set_version('0.1')
        about_dialog.set_comments(u'Check for Linux Lite updates')
        about_dialog.set_authors([u'Brian Tomlinson <brian.tomlinson@linux.com>'])
        about_dialog.run()
        about_dialog.destroy()

    def show_log(self, widget):
        subprocess.Popen('/usr/bin/leafpad /tmp/liteupdater.log', shell=True)


if __name__ == '__main__':
    SystrayApp()
    Gtk.main()
