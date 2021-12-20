#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import socket
from . import comand_1c


class IbcmdFileBase(comand_1c.RunnerParams):
    def __init__(self, **kwargs):
        super(IbcmdFileBase, self).__init__()
        self.bparams = ['--db-path={}'.format(kwargs["base"])]
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
        self.bparams.append("--user=" + kwargs["usr"])
        self.bparams.append("--password=" + kwargs["pwd"])


class ClusterBase(object):
    def __init__(self, **kwargs):
        super(ClusterBase, self).__init__()
        self.cluster = kwargs['cluster']
        self.infobase = kwargs['infobase']
        self.usr = kwargs['usr']
        self.pwd = kwargs['pwd']


class DesignerPostgresBase(comand_1c.RunnerParams):
    def __init__(self, **kwargs):
        super(DesignerPostgresBase, self).__init__()
        server = kwargs["srv"] if hasattr(kwargs, "srv") else kwargs["server"]
        self.bparams = []
        self.bparams.append('/S "{0}\{1}"'.format(server, kwargs["base"]))
        self.bparams.append('/N "{0}"'.format(kwargs["usr"]))
        if kwargs["pwd"]:
            self.bparams.append('/P "{0}"'.format(kwargs["pwd"]))

    def get_process_template(self):
        return self.bparams[0]


class DesignerFileBase(comand_1c.RunnerParams):
    def __init__(self, **kwargs):
        super(DesignerFileBase, self).__init__()
        self.bparams = []
        self.bparams = ['/F "{0}"'.format(kwargs["base"])]
        self.bparams.append('/N "{0}"'.format(kwargs["usr"]))
        if kwargs["pwd"]:
            self.bparams.append('/P "{0}"'.format(kwargs["pwd"]))

    def get_process_template(self):
        return self.bparams[0]


def get_ibcmd_base(**kwargs):
    if kwargs["type"] == "postgres":
        return IbcmdPostgresBase(**kwargs)
    else:
        return IbcmdFileBase(**kwargs)


def get_designer_base(**kwargs):
    if kwargs["type"] == "postgres":
        return DesignerPostgresBase(**kwargs)
    else:
        return DesignerFileBase(**kwargs)
