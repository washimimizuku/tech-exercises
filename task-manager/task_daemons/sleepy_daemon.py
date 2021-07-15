import time

from daemons.prefab import run


class SleepyDaemon(run.RunDaemon):

    def run(self):

        while True:

            time.sleep(1)
