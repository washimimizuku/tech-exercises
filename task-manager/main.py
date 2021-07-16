#!/usr/bin/env python

import sys

from task_manager import TaskManager
from process import Process


if __name__ == '__main__':

    limit = int(sys.argv[1])
    fifo = sys.argv.count('--fifo') > 0
    by_priority = sys.argv.count('--by_priority') > 0

    task_manager = TaskManager(limit, fifo, by_priority)

    while True:
        action = input('> ')

        if action[:4] == "add ":
            priority = action.split()[1]
            if (priority != "low" and priority != "medium" and priority != "high"):
                print(
                    f"Priority '{priority}' is not valid. Please choose one of [low, medium, high].")
            else:
                task_manager.add_process(priority)

        elif action == "list":
            task_manager.list_processes()

        elif action[:5] == "kill ":
            pid = int(action.split()[1])
            task_manager.kill_process(pid)

        elif action[:10] == "killgroup ":
            priority = action.split()[1]
            if (priority != "low" and priority != "medium" and priority != "high"):
                print(
                    f"Priority '{priority}' is not valid. Please choose one of [low, medium, high].")
            else:
                task_manager.kill_processes(priority)

        elif action == "killall":
            task_manager.kill_all_processes()

        elif action == "quit":
            task_manager.kill_all_processes()
            break

        else:
            print("Command not found, try again.")
