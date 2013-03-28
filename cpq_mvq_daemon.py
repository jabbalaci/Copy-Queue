#!/usr/bin/env python

"""
Daemon for the cpq and mvq commands.

It is not running all the time. cpq and mvq will start it
if it's not running. It will run as long as there are tasks.
When all tasks are done, the daemon stops.
Since tasks are added by cpq/mvq, the daemon will be started
by those commands if necessary.
Only one instance of the daemon may run, it is achieved via
a lock file.
"""

import os
import sys
import config as cfg
from mylogging import debug, info
import atexit
from time import sleep


def process():
    """
    Take a task, execute it, then remove it.

    Check the task directory. If there are no tasks, return None (and the daemon
    will stop).
    If there is a task, execute it and then remove it. In this case return True.
    """
    batches = [t for t in os.listdir(cfg.QDIR) if len(t)==4 and t.isdigit()]
    if len(batches) == 0:
        return None

    # else
    first = sorted(batches)[0]
    fpath = "{qdir}/{fname}".format(qdir=cfg.QDIR, fname=first)

    info('start: process {fname}:'.format(fname=first))
    with open(fpath) as f:
        for line in f:
            info("    " + line.rstrip("\n"))
    # sleep(10)    # used for tests
    os.system(fpath)
    info('end: process {fname}'.format(fname=first))

    os.unlink(fpath)
    return True


def check_lock():
    """
    Check the lock file.

    If there is a lock file, then the daemon is running and this
    instance will quit.
    If there is no lock file, then this instance will be the running
    daemon. In this case the lock file is created.
    """
    if os.path.exists(cfg.LOCK):
        debug('daemon already running; not starting another instance')
        sys.exit()
    # else
    os.system("touch {lock}".format(lock=cfg.LOCK))


def cleanup():
    """
    The daemon stops properly.

    Let's remove the lock file.
    """
    remove_lock()


def remove_lock():
    """
    Remove the lock file.

    When there are no more tasks, the daemon stops and removes
    the lock file.
    """
    if os.path.exists(cfg.LOCK):
        os.unlink(cfg.LOCK)


def main():
    """
    Controller.

    If there is no running daemon, then let's start working.
    Process every task and wait a little bit after each.
    The producer(s) may create lots of small tasks that are
    processed very fast, thus we wait a little bit.
    When all tasks are treated, we quit.
    """
    check_lock()
    debug("="*50)
    debug('start daemon')
    #
    while process():
        sleep(0.05)
    #
    debug('stop daemon')
    remove_lock()

#############################################################################

if __name__ == "__main__":
    atexit.register(cleanup)
    main()