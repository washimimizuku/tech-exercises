import logging
import multiprocessing
import os
import time

from datetime import datetime


logfile = os.path.join(os.getcwd(), "task_manager.log")
logging.basicConfig(filename=logfile, level=logging.DEBUG)


def daemon():

    while True:
        time.sleep(1)
        logging.info(f'Running process with pid {os.getpid()} ...')


class Process:
    def __init__(self, priority):
        self.pid = 0
        self.priority = priority
        self.created_at = datetime.now()
        self.proc = multiprocessing.Process(target=daemon, args=())
        self.proc.daemon = True
        self.proc.start()
        self.pid = self.proc.pid

    def stop(self):
        self.proc.kill()
