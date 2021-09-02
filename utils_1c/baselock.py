#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from . import comand_runner


class BaseLock(comand_runner.Runner):
    """block base to make safe backup"""

    def __init__(self, *args, cmd_func=lambda x: print(x), cmd_pach="TEST_PACH"):
        super(BaseLock, self).__init__()
        comand_runner.Runner.__init__(self, *args, cmd_func=cmd_func, cmd_pach=cmd_pach)
        self.locked = False

    def __enter__(self):
        cmd = " --sessions-deny=on --scheduled-jobs-deny=on"
        cmd = cmd + '--denied-message="BaseLock in progress"'
        self.run("infobase", cmd)
        self.locked = True
        return self

    def __exit__(self, type1, value, traceback):
        if self.locked:
            cmd = " --sessions-deny=off --scheduled-jobs-deny=off"
            self.run(cmd)
            self.locked = False
