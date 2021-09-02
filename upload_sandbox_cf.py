#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""upload .cf from local to sandbox"""

from utils_1c import ibcmd
from sets_1c import settings_1c
from sets_1c import connection_1c
from sets_1c import argparse_1c
from utils_1c import comand_runner
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
sandbox = "{}/{}".format(parser.args["sandbox"][0], parser.b[0])

platform = "deb"
sets = settings_1c.Settings()
ibcmd_pach = sets.ibcmd_pach[platform]
ibcmd = comand_runner.Runner('--db-path={}'.format(parser.args["pach"][0]),
                            cmd_func=lambda x: os.system(x),
                            cmd_pach=ibcmd_pach)

tmpfile = settings_1c.FileManager().tmpf("/tmp", parser.b[0], "cf")
ibcmd.run("infobase config save", tmpfile)
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
