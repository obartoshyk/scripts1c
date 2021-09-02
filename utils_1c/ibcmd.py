#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from sets_1c import settings_1c
from utils_1c import comand_runner
import socket

def get_postgres_bparams(srv, base, usr, pwd):
    bparams = ["--dbms=postgresql"]
    bparams.append("--db-server=" + socket.gethostbyname(srv))
    bparams.append("--db-name=" + base)
    bparams.append("--db-user=" + usr)
    bparams.append("--db-pwd=" + pwd)
    return bparams


def get_file_bparams(pach):
    return ['--db-path={}'.format(pach)]

platform = "deb"
sets = settings_1c.Settings()
ibcmd_pach = sets.ibcmd_pach[platform]


