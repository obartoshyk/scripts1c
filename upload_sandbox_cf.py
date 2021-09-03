#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""upload .cf from local to sandbox"""

from sets_1c import settings_1c
from sets_1c import comand_1c
from utils_1c import config
from utils_1c import basedata
from sets_1c import argparse_1c
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


local_Config = config.Config(*local_base.getparams())
    #cmd_func=lambda x: os.system(x))
tmpf = local_Config.config_save()

"""
with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
    if not conn.testmode:
        ftp = conn.ssh.open_sftp()
        print("uploading to {}".format(parser.s[0]))
        ftp.put(tmpfile, tmpfile)
        os.remove(tmpfile)

    oIbSrv = regibsrv.IbSrv(base=parser.args["base"][0],
                            pach=parser.args["sandbox"][0],
                            test=parser.args["test"])
    rIbCmd = ibcmd.IbCmd(
        cmd_func=lambda x: conn.cast(x),
        bparams=ibcmd.get_file_bparams(sandbox),
        platform="deb")
    oIbSrv.remote("stop", conn)
    rIbCmd.run("infobase config load", tmpfile)
    rIbCmd.run("infobase config apply", "--force")
    oIbSrv.remote("start", conn)
    if not conn.testmode:
        ftp.remove(tmpfile)
        ftp.close()"""
