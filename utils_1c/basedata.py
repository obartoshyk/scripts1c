#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from sets_1c import comand_1c
import socket

class IbcmdFileBase(comand_1c.RunnerParams):
    def __init__(self, cat_pach=""):
        super(IbcmdFileBase, self).__init__()
        self.bparams = ['--db-path={}'.format(cat_pach)]


class IbcmdPostgresBase(comand_1c.RunnerParams):
    def __init__(self, srv="", base="", usr="", pwd=""):
        super(IbcmdFileBase, self).__init__()
        self.bparams = ["--dbms=postgresql"]
        self.bparams.append("--db-server=" + socket.gethostbyname(srv))
        self.bparams.append("--db-name=" + base)
        self.bparams.append("--db-user=" + usr)
        self.bparams.append("--db-pwd=" + pwd)