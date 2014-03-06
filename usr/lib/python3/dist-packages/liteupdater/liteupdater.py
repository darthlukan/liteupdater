#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
from gi.repository import Gtk


class SystrayApp(object):

    def __init__(self):
        self.tray = Gtk.StatusIcon()
        self.menu = Gtk.Menu()
        self.menu_about = Gtk.MenuItem()
        self.menu_quit = Gtk.MenuItem()
        self.about_dialog = ''

        if os.path.isfile('/usr/share/pixmaps/updaten.png'):
            self.tray.set_from_file('/usr/share/pixmaps/updaten.png')
        else:
            self.tray.set_from_stock(Gtk.STOCK_ABOUT)

        self.tray.set_tooltip_text('Lite Updater')
        self.tray.connect('popup-menu', self.on_right_click)

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(icon, event_button, event_time)

    def make_menu(self, icon, event_button, event_time):

        try:
            for widget in self.menu.get_children():
                self.menu.remove(widget)
        except Exception as e:
            print(e)

        self.menu_about.set_label("About")
        self.menu_about.connect('activate', self.show_about_dialog)

        self.menu_quit.set_label("Quit")
        self.menu_quit.connect("activate", Gtk.main_quit)

        self.menu.append(self.menu_about)
        self.menu.append(self.menu_quit)

        self.menu.show_all()

        def pos(menu, icon):
            return Gtk.StatusIcon.position_menu(menu, icon)

        self.menu.popup(None, None, pos, icon, event_button, event_time)

    def show_about_dialog(self, widget):
        self.about_dialog = Gtk.AboutDialog()
        self.about_dialog.set_destroy_with_parent(True)
        self.about_dialog.set_icon_name('Lite Updater')
        self.about_dialog.set_name('Lite Updater')
        self.about_dialog.set_version('0.1')
        self.about_dialog.set_comments(u'Check for Linux Lite updates')
        self.about_dialog.set_authors([u'Brian Tomlinson <brian.tomlinson@linux.com>'])
        self.about_dialog.run()
        self.about_dialog.destroy()

    def show_log(self, widget):
        subprocess.Popen('/usr/bin/leafpad /tmp/liteupdater.log', shell=True)


if __name__ == '__main__':
    SystrayApp()
    Gtk.main()
