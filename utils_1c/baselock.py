#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
class BaseLock(object):
    """block base to make safe backup"""

    def __init__(self, server1c, base, usr, pwd):
        super(BaseLock, self).__init__()
        self.server = server1c
        self.base = base
        self.locked = False
        self.usr = usr
        self.pwd = pwd

    def __enter__(self, base, usr, pwd):
        cmd = "infobase --cluster={cluster} update --infobase={infobase}"
        cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
        cmd = cmd + " --sessions-deny=on --scheduled-jobs-deny=on"
        cmd = cmd + '--denied-message="backup in progress"'
        cmd = cmd.format(**self.server.get_base(self.base))
        self.server.run(cmd)
        self.locked = True
        return self

    def __exit__(self, type1, value, traceback):
        if self.locked:
            cmd = "infobase --cluster={cluster} update --infobase={infobase}"
            cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
            cmd = cmd + " --sessions-deny=off --scheduled-jobs-deny=off"
            cmd = cmd.format(**self.server.get_base(self.base))
            self.server.run(cmd)
            self.locked = False
