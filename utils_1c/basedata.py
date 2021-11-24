#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import socket
from . import comand_1c


class IbcmdFileBase(comand_1c.RunnerParams):
    def __init__(self, **kwargs):
        super(IbcmdFileBase, self).__init__()
        self.bparams = ['--db-path={}'.format(kwargs["cat_pach"])]
        if kwargs["usr"]:
            self.bparams.append("--user=" + kwargs["usr"])
        if kwargs["pwd"]:
            self.bparams.append("--password=" + kwargs["pwd"])


class IbcmdPostgresBase(comand_1c.RunnerParams):
    def __init__(self, **kwargs):
        super(IbcmdPostgresBase, self).__init__()
        self.bparams = ["--dbms=postgresql"]
        self.bparams.append("--db-server=" + socket.gethostbyname(kwargs["srv"]))
        self.bparams.append("--db-name=" + kwargs["base"])
        self.bparams.append("--db-user=" + kwargs["db_usr"])
        self.bparams.append("--db-pwd=" + kwargs["db_pwd"])


class ClusterBase(object):
    def __init__(self, **kwargs):
        super(ClusterBase, self).__init__()
        self.cluster = kwargs['cluster']
        self.infobase = kwargs['infobase']
        self.usr = kwargs['usr']
        self.pwd = kwargs['pwd']


def get_ibcmd_base(**kwargs):
    if kwargs["type"] == "postgres":
        return IbcmdPostgresBase(**kwargs)
    else:
        return IbcmdFileBase(**kwargs)
