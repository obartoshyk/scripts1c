#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" config load : update base config, block base before
    config save : backup base config, block base before
    config import
    config export
    config export --sync
    config apply --force
    dump
    restore
"""
from utils_1c import basedata, connection_1c, argparse_1c, infobase_comand


def config_run(icomand, method, tmpfile=""):
    methods = {
        "save": ["config_save"],
        "load": ["config_load", "config_apply"],
        "export_sync": ["config_export_sync"],
        "export": ["config_export"],
        "import": ["config_import", "config_apply"],
        "dump": ["dump"],
        "restore": ["restore"]
    }
    method_list = methods[method]
    print(getattr(icomand, method_list[0])(tmpfile))
    if len(method_list) > 1:
        print(getattr(icomand, method_list[1])())


parser = argparse_1c.ArgumentParser_1C("sbkduf", description=__doc__)
parser.add_argument('-m', '--method',
                    metavar="MTD",
                    help='save/export/load/import',
                    nargs=1, type=str, default="save", required=False)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='pach to file',
                    nargs=1, type=str, required=False)
parser.decode_arg()

for srv_name in parser.args["server"]:
    with connection_1c.Connection(srv=srv_name, **parser.args) as conn:
        for base_name in parser.args["base"]:
            ibcmd_base = basedata.get_ibcmd_base(base=base_name, type="file", srv=srv_name,
                                                 cat_pach=base_name,
                                                 usr=parser.usr, pwd=parser.pwd,
                                                 db_usr=parser.db_usr, db_pwd=parser.db_pwd)

            i_comand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                                       cmd_func=conn.cast)
            config_run(i_comand, parser.args["method"][0], parser.args["pach"][0])
