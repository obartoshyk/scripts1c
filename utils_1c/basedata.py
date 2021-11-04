#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import socket
from . import comand_1c


class IbcmdFileBase(comand_1c.RunnerParams):
    def __init__(self, cat_pach=""):
        super(IbcmdFileBase, self).__init__()
        self.bparams = ['--db-path={}'.format(cat_pach)]


class IbcmdPostgresBase(comand_1c.RunnerParams):
    def __init__(self, srv="", base="", db_usr="", db_pwd=""):
        super(IbcmdPostgresBase, self).__init__()
        self.bparams = ["--dbms=postgresql"]
        self.bparams.append("--db-server=" + socket.gethostbyname(srv))
        self.bparams.append("--db-name=" + base)
        self.bparams.append("--db-user=" + db_usr)
        self.bparams.append("--db-pwd=" + db_pwd)


class ClusterBase(object):
    def __init__(self, cluster="", base="", usr="", pwd=""):
        super(ClusterBase, self).__init__()
        self.cluster = cluster
        self.base = base
        self.usr = usr
        self.pwd = pwd