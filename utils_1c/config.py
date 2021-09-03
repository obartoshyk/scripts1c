#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""upload .cf from local to sandbox"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from sets_1c import settings_1c
from sets_1c import comand_1c
import basedata


class Config(comand_1c.CommandMaker):
    """ config load : update base config, block base before
        config save : backup base config, block base before
        config import
        config export
        config apply --force
    """

    def __init__(self, *args, **kwargs):
        comand_1c.CommandMaker.__init__(self, *args, command="ibcmd", **kwargs)

    def config_save(self, tmpfile=""):
        if not tmpfile:
            tmpfile = settings_1c.FileManager().tmpf("/tmp", "TPM_save", "cf")
        self.run("infobase config save", tmpfile)
        return tmpfile

    def config_load(self, tmpfile):
        self.run("infobase config load", tmpfile)

    def config_export(self, tmpfile):
        self.run("infobase config export", tmpfile)

    def config_import(self, tmpfile):
        self.run("infobase config import", tmpfile)

    def config_apply(self):
        self.run("infobase config apply", "--force")

    def config_run(self, method, tmpfile=""):
        methods = {
            "save": ["config_save"],
            "load": ["config_load", "config_apply"],
            "export": ["config_export"],
            "import": ["config_import", "config_apply"]
        }
        method_list = methods[method]
        getattr(self, method_list[0])(tmpfile)
        if len(method_list) > 1:
            getattr(self, method_list[1])()


if __name__ == "__main__":
    from sets_1c import argparse_1c

    parser = argparse_1c.ArgumentParser_1C("sbkd", description=__doc__)
    parser.add_argument('-m', '--method',
                        metavar="MTD",
                        help='save/export/load/import',
                        nargs=1, type=str, default="save", required=False)
    parser.add_argument('-p', '--pach',
                        metavar="PACH",
                        help='pach to file',
                        nargs=1, type=str, required=False)
    parser.add_argument('-f', '--platform',
                        metavar="DEB",
                        help='deb/win',
                        nargs=1, type=str, default="deb", required=False)
    parser.decode_arg()
    if parser.s[0] == "localhost":
        if parser.args["test"]:
            def cmd_func(x): print(x)
        else:
            def cmd_func(x): os.system(x)

        local_base = basedata.IbcmdFileBase(parser.b[0])
        lConfig = Config(*local_base.getparams(),
                         cmd_func=cmd_func,
                         platform=parser.args["platform"])

        lConfig.config_run(parser.args["method"][0], parser.args["pach"][0])
    else:
        from sets_1c import connection_1c
        with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
            if parser.args["test"]:
                def cmd_func(x): print(x)
            else:
                def cmd_func(x): conn.cast(x)
            remote_base = basedata.IbcmdPostgresBase(
                srv=parser.s[0],
                base=parser.b[0],
                db_usr=parser.db_usr,
                db_pwd=parser.db_pwd
            )
            lConfig = Config(*remote_base.getparams(),
                             cmd_func=cmd_func,
                             platform=parser.args["platform"])
            lConfig.config_run(parser.args["method"][0], parser.args["pach"][0])

