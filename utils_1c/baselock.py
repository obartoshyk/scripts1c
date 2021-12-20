#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from . import comand_1c


class LockCommandMaker(object):
    def __init__(self, clbase):
        super(LockCommandMaker, self).__init__()
        self.cb = clbase

    def get_block(self, uc):
        tmpl = "infobase --cluster={}" \
              " update --infobase={}" \
              " --infobase-user={}" \
              " --infobase-pwd={}" \
              " --sessions-deny=on" \
              " --scheduled-jobs-deny=on" \
              ' --denied-message="denied by 1cbot"'
        cmd = tmpl.format(self.cb.cluster, self.cb.infobase, self.cb.usr, self.cb.pwd)
        if uc:
            pc = "--permission-code={}".format(uc)
            return " ".join([cmd, pc])
        return cmd

    def get_unblock(self):
        cmd = "infobase --cluster={}" \
              " update --infobase={}" \
              " --infobase-user={} " \
              "--infobase-pwd={}" \
              " --sessions-deny=off --scheduled-jobs-deny=off"
        return cmd.format(self.cb.cluster, self.cb.infobase, self.cb.usr, self.cb.pwd)


class BaseLock(comand_1c.CommandMaker):
    """block base to make safe backup"""

    def __init__(self, clbase, **kwargs):
        super(BaseLock, self).__init__()
        comand_1c.CommandMaker.__init__(self, command="rac", **kwargs)
        self.cmaker = LockCommandMaker(clbase)
        self.locked = False
        try:
            self.uc = kwargs["uc"]
        except:
            self.uc = ""

    def __enter__(self):
        self.block()
        return self

    def __exit__(self, type1, value, traceback):
        if self.locked:
            self.unblock()

    def block(self):
        self.run(self.cmaker.get_block(self.uc))
        self.locked = True
        return self.locked

    def unblock(self):
        self.run(self.cmaker.get_unblock())
        self.locked = False
        return self.locked
