#!/usr/bin/env python

import logging
import multiprocessing
import os
import sys
import time


logfile = os.path.join(os.getcwd(), "task_manager.log")
logging.basicConfig(filename=logfile, level=logging.DEBUG)


def daemon():

    while True:
        time.sleep(1)
        logging.info(f'running process with pid {os.getpid()} ...')


class TaskManager:
    def __init__(self, limit):
        self.processes = []
        self.limit = limit

    def add_process(self, level):
        if (len(self.processes) < self.limit):
            process = Process(level)
            self.processes.append(process)
            print(f'Added process {process.pid}')
        else:
            print(f'Limit of {self.limit} processes reached')

    def list_processes(self):
        for process in self.processes:
            print(f'{process.pid} | {process.priority} | {process.proc.is_alive()}')

    def kill_process(self, pid):
        for index, process in enumerate(self.processes):
            if process.pid == pid:
                process.stop()
                del self.processes[index]
                return

    def kill_processes(self, priority):
        to_delete = []
        for index, process in enumerate(self.processes):
            if process.priority == priority:
                to_delete.append(index)
                process.stop()

        for index in reversed(to_delete):
            del self.processes[index]

    def kill_all_processes(self):
        for process in self.processes:
            process.stop()
        self.processes = []


class Process:
    def __init__(self, priority):
        self.pid = 0
        self.priority = priority
        self.proc = multiprocessing.Process(target=daemon, args=())
        self.proc.daemon = True
        self.proc.start()
        self.pid = self.proc.pid

    def stop(self):
        self.proc.kill()


if __name__ == '__main__':

    limit = int(sys.argv[1])

    while True:
        action = input('> ')

        if action[:4] == "add ":
            level = action.split()[1]
            task_manager.add_process(level)

        elif action == "list":
            task_manager.list_processes()

        elif action[:5] == "kill ":
            pid = int(action.split()[1])
            task_manager.kill_process(pid)

        elif action[:10] == "killgroup ":
            priority = action.split()[1]
            task_manager.kill_processes(priority)

        elif action == "killall":
            task_manager.kill_all_processes()

        elif action == "quit":
            task_manager.kill_all_processes()
            break

        else:
            print("Command not found, try again")
