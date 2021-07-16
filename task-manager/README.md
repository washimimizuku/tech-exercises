# Task Manager

A simple task manager to manager system processes.

## Installation

```
pipenv shell
pipenv install
```

## Usage

To launch the task manager interactive shell in a simple way, run the following command:

```
python main.py 5
```

The arguments for the command are:

```
python main.py {limit} [--fifo] [--by_priority]
```

- Limit (mandatory): Maximum number of processes.
- --fifo (optional): When maximum number of processes is reached, replace the oldest process with the new one.
- --by_priority (optional): When maximum number of processes is reached, replace a lower priority process with the new one.

When both --fifo and --by_priority are set, the task manager ignores the --fifo option.

## Interactive shell

The shell supports the following commands:

- add {priority} - Adds a new process. Priority must be one of: [low, medium, high].
- list - Lists all processes.
- kill {pid} - Kills process with the given PID.
- killgroup {priority} - Kills all processes that have the given priority. Priority must be one of: [low, medium, high].
- killall - Kills all processes.
- quit - Quits the interactive shell.

Note: The output of the processes will be logged on the file task_manager.log
