#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import time
import subprocess
import logging
import notify2


def send_notification(title, body):
    """
    This function uses notify2 to send DBUS notifications.

    Params:
        title (str)
        body (str)

    returns notify2.Notification().show() (boolean)
    """
    notify2.init("Lite Updater")
    return notify2.Notification(title, body).show()


def sync_caches():
    """
    Uses subprocess to call 'apt-get update'. See man apt-get(8)
    for more info on the apt-get command.

    Returns boolean
    """
    title = "Syncing repositories..."
    # TODO: This call will fail due to lack of permissions. Gracefully elevate.
    upd_output = subprocess.Popen("apt-get update", shell=True, stdout=subprocess.PIPE)

    if len(upd_output.stdout) > 10:  # we're just checking for failed execution to start.
        body = "Ran update"
    else:
        body = "There was an error syncing the repositories!"
        send_notification(title, body)
        return False

    send_notification(title, body)
    return True


def check_updateables(*args):
    """
    Calls sync_caches and then checks the number of available updates
    based on the packages listed in stdout after 'apt-show-versions -u'.

    See man apt-show-versions for more info on this command.

    Returns num_updateables, pkgs (int, list (strings))
    """
    sync_caches()
    title = "Checking for available updates..."
    body = "searching..."
    send_notification(title, body)
    pkgs = []

    chk_output = subprocess.Popen("apt-show-versions -u", shell=True, stdout=subprocess.PIPE)

    for pkg in chk_output.stdout:
        pkg.rstrip('\r\n')
        pkgs.append(pkg)

    num_updatables = len(pkgs)

    if num_updatables >= 1:
        title = "Updates available!"
        body = "You have %s updates available for installation." % num_updatables
        send_notification(title, body)
    else:
        title = "No updates available."
        body = "Your system is up-to-date!"
        send_notification(title, body)

    return num_updatables, pkgs


def perform_update():
    # TODO: Base logic for executing updates (# apt-get upgrade).
    pass


def main():
    raise NotImplementedError


if __name__ == '__main__':
    main()
