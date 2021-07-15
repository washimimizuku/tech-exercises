#!/usr/bin/env python

import logging
import os
import sys

from task_daemons import sleepy_daemon


if __name__ == '__main__':

    action = sys.argv[1]
    logfile = os.path.join(os.getcwd(), "sleepy.log")
    pidfile = os.path.join(os.getcwd(), "sleepy.pid")

    logging.basicConfig(filename=logfile, level=logging.DEBUG)
    d = sleepy_daemon.SleepyDaemon(pidfile=pidfile)

    if action == "start":

        d.start()

    elif action == "stop":

        d.stop()

    elif action == "restart":

        d.restart()
