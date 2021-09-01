#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from . import settings_1c
import socket

def get_postgres_bparams(srv, base, usr, pwd):
    bparams = ["--dbms=postgresql"]
    bparams.append("--db-server=" + socket.gethostbyname(srv))
    bparams.append("--db-name=" + base)
    bparams.append("--db-user=" + usr)
    bparams.append("--db-pwd=" + pwd)
    return bparams

def get_file_bparams(pach):
    return ["--db-path={}".format(pach)]

class IbCmd(object):
    """ IbCmd server utils"""

    def __init__(self, cmd_func, bparams, platform="deb", test=True):
        super(IbCmd, self).__init__()
        sets = settings_1c.Settings()
        self.cmd_func = cmd_func
        self.test = test
        self.bparams = bparams
        self.ibcmd_pach = sets.ibcmd_pach[platform]

    def run(self, cmd):
            if not self.test:
                print("run: {}".format(cmd))
                self.cmd_func(cmd)
            else:
                print("run(TEST): {}".format(cmd))

    def create_cmd(self, cmd0, *args):
        return "{0} {1} {2}".format(self.ibcmd_pach, cmd0, " ".join([*self.bparams, *args]))