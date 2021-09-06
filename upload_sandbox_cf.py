#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""upload .cf from local to sandbox"""

from utils_1c import config
from utils_1c import basedata
from sets_1c import connection_1c
from sets_1c import argparse_1c
import regibsrv
import os

parser = argparse_1c.ArgumentParser_1C("sbk", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='local base pach',
                    nargs=1, type=str, required=True)
parser.add_argument('-n', '--sandbox',
                    metavar="PACH",
                    help='sandbox base pach',
                    nargs=1, type=str, required=True)
parser.decode_arg()

local_base = basedata.IbcmdFileBase(parser.args["pach"][0])
sandbox_base = basedata.IbcmdFileBase("{}/{}".format(parser.args["sandbox"][0], parser.b[0]))

if parser.args["test"]:
    def lcmd_func(x):
        print(x)
else:
    def lcmd_func(x):
        os.system(x)
local_Config = config.Config(*local_base.getparams(),
                             cmd_func=lcmd_func)
tmpfile = local_Config.config_save()


with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
    if parser.args["test"]:
        def cmd_func(x):
            print(x)
    else:
        ftp = conn.ssh.open_sftp()
        print("uploading to {}".format(parser.s[0]))
        ftp.put(tmpfile, tmpfile)
        os.remove(tmpfile)

        def cmd_func(x):
            conn.cast(x)

    remote_Config = config.Config(*sandbox_base.getparams(), cmd_func=cmd_func)

    oIbSrv = regibsrv.IbSrv(base=parser.args["base"][0],
                            pach=parser.args["sandbox"][0],
                            test=parser.args["test"])

    oIbSrv.remote("stop", conn)
    tmpfile = remote_Config.config_load(tmpfile)
    oIbSrv.remote("start", conn)
    if not conn.testmode:
        ftp.remove(tmpfile)
        ftp.close()
