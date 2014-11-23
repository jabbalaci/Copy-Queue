#!/usr/bin/env python

"""
copy queue (cpq), move queue (mvq)

This is an extension of the Unix cp and mv commands. These commands
(cpq and mvq) put tasks in a queue, thus you have the following
advantages:
1) When you launch one of these commands, you get the prompt back
   immediately.
2) You can launch as many copy/move tasks as you want. Since they
   are in a queue, one will be executed after the other. It is
   easy on resources since only one operation is executed at a given
   time.

Slow down production a bit
==========================

If you call cpq/mvq in a loop and you add lots of small files
that can be copied/moved quickly, then add some pause in the
loop, i.e. don't produce tasks like a crazy. Example:

    for f in your_list:
        cmd = '/path/to/cpq "{f}" /copy/to/'.format(f=f)
        print cmd
        os.system(cmd)
        sleep(0.05)    # ADD THIS PAUSE!

Too fast production can cause problems.

Usage:
======

Put two symbolic links on this file. The links must be
called "cpq" and "mvq".
Then use cpq and mvq like cp and mv. cpq and mvq will
call cp and mv actually, thus you can use any options
that are accepted by cp and mv.

Example:
========

    cpq cd1.avi /mnt/usb/movies/
    cpq cd2.avi /mnt/usb/movies/
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import os
import sys

import config as cfg

CPQ = 'cp'
MVQ = 'mv'
COMMAND = None    # will be set later
THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def check_dir(dirname):
    if not os.path.isdir(dirname):
        print("Error: {d} is not a directory or doesn't exist."
              .format(d=cfg.QDIR))
        sys.exit(1)


def check_daemon():
    if not os.path.isfile(cfg.DAEMON):
        print("Error: the daemon script is not found.")
        print("It should be here: {path}".format(path=cfg.DAEMON))
        sys.exit(1)


def check_scriptname(s):
    global COMMAND
    #
    fname = os.path.split(s)[1]
    if fname == 'cpq':
        COMMAND = CPQ
    elif fname == 'mvq':
        COMMAND = MVQ
    else:
        print("Error: the script cpq_mvq.py cannot be called directly.")
        print("You should put two links on it called 'cpq' and 'mvq'.")
        sys.exit(1)


def check_params(params):
    if len(params) == 0:
        print("Error: you didn't specify any parameters.")
        sys.exit(1)


def get_next_id():
    li = os.listdir(cfg.QDIR)
    li = [int(t) for t in li if len(t) == 4 and t.isdigit()]
    if not li:
        return '0001'
    else:
        next_id = str(max(li)+1).zfill(4)
        if int(next_id) > 9999:
            print("Error: there are too many tasks in {qdir}."
                  .format(qdir=cfg.QDIR))
            print("Tip: do some cleaning in that directory.")
            sys.exit(1)
        # else
        return next_id


def start_daemon():
    """
    Start the daemon.

    It will start the daemon only if it's not running.
    """
    if os.path.exists(cfg.LOCK):
        return
    # else
    os.system("{daemon} &".format(daemon=cfg.DAEMON))


def shellquote(s):
    """
    Quote the parameters for cp and mv.
    """
    return "'" + s.replace("'", "'\\''") + "'"


def process(task_id, args):
    """
    For each file create an executable batch file.

    These batch files will be executed by the daemon.
    """
    fname = "{qdir}/{task}".format(qdir=cfg.QDIR, task=task_id)
    with open(fname, "w") as f:
        print >>f, 'cd {dir}'.format(dir=shellquote(os.getcwd()))
        args = [shellquote(s) for s in args]
        print >>f, "{cmd} {params}".format(cmd=COMMAND, params=' '.join(args))
    os.chmod(fname, 0o700)
    #
    start_daemon()


def main():
    check_dir(cfg.QDIR)
    check_scriptname(sys.argv[0])
    check_params(sys.argv[1:])
    check_daemon()
    #
    next_id = get_next_id()
    process(next_id, sys.argv[1:])

#############################################################################

if __name__ == "__main__":
    main()
