#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gtk
import subprocess


class SystrayApp(object):
    def __init__(self):
        self.tray = gtk.StatusIcon()
        self.tray.set_from_file('/usr/share/pixmaps/updaten.png')
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.set_tooltip('Lite Updater')

    def on_right_click(self, icon, event_button, event_time):
        self.make_menu(event_button, event_time)
        if self.tray.set_blinking():
            self.tray.set_blinking(False)
            self.tray.set_from_file('/usr/share/icons/updaten.png')

    def make_menu(self, event_button, event_time):
        menu = gtk.Menu()

        about = gtk.MenuItem('About')
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

        run = gtk.MenuItem('Check Updates')
        run.show()
        menu.append(run)

        chklog = gtk.MenuItem('View Log')
        chklog.show()
        menu.append(chklog)
        chklog.connect('activate', self.show_log)

        quit_action = gtk.MenuItem('Quit')
        quit_action.show()
        menu.append(quit_action)
        quit_action.connect('activate', gtk.main_quit)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   event_button, event_time, self.tray)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
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
    gtk.main()
