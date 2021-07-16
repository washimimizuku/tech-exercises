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
    def __init__(self, limit, fifo, by_priority):
        self.processes = []
        self.limit = limit
        self.fifo = fifo
        self.by_priority = by_priority

    def _create_process(self, level):
        process = Process(level)
        self.processes.append(process)
        print(f'Added process {process.pid}')

    def add_process(self, level):
        if (len(self.processes) < self.limit):
            self._create_process(level)
        elif (self.by_priority):
            can_create_process = True
            process_to_terminate = -1

            if level == 'low':
                can_create_process = False
            else:
                low = []
                medium = []
                high = []
                for index, process in enumerate(self.processes):
                    if process.priority == 'low':
                        low.append(index)
                    elif process.priority == 'medium':
                        medium.append(index)
                    elif process.priority == 'high':
                        high.append(index)

                if level == 'medium' and len(low) > 0:
                    process_to_terminate = low[0]
                elif level == 'high' and len(medium) > 0:
                    process_to_terminate = medium[0]
                else:
                    can_create_process = False

            if can_create_process:
                self.processes[process_to_terminate].stop()
                del self.processes[process_to_terminate]

                self._create_process(level)
            else:
                print(
                    f'Limit of {self.limit} processes reached and no lower process found')

        elif (self.fifo):
            self.processes[0].stop()
            del self.processes[0]

            self._create_process(level)
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
                print(f'Killed process {process.pid}')
                return

    def kill_processes(self, priority):
        to_delete = []
        for index, process in enumerate(self.processes):
            if process.priority == priority:
                to_delete.append(index)
                process.stop()
                print(f'Killed process {process.pid}')

        for index in reversed(to_delete):
            del self.processes[index]

    def kill_all_processes(self):
        for process in self.processes:
            process.stop()
            print(f'Killed process {process.pid}')
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
    fifo = sys.argv.count('--fifo') > 0
    by_priority = sys.argv.count('--by_priority') > 0

    task_manager = TaskManager(limit, fifo, by_priority)

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
