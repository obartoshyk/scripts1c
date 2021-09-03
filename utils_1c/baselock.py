#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sets_1c import comand_1c


class BaseLock(comand_1c.Runner):
    """block base to make safe backup"""

    def __init__(self, *args, **kwargs):
        super(BaseLock, self).__init__()
        comand_1c.Runner.__init__(self, *args, **kwargs)
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
