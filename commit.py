#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import basedata, connection_1c, argparse_1c, infobase_comand, rep


def cast_cmd_list(cn, cmd_list):
    for cm in cmd_list:
        print(cn.cast(cm))


parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-e', '--text',
                    metavar="TXT",
                    help='AUT-2000',
                    nargs=1, type=str, default="save", required=True)
parser.decode_arg()

srv = parser.args["server"][0]
base = parser.args["base"][0]

with connection_1c.Connection(srv=srv, **parser.args) as conn:
    ibcmd_base = basedata.get_ibcmd_base(base=base, type="file", srv=srv,
                                         cat_pach=base,
                                         usr=parser.usr, pwd=parser.pwd,
                                         db_usr=parser.db_usr, db_pwd=parser.db_pwd)

    i_comand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                               cmd_func=conn.cast)
    repo = rep.Repository(parser)
    print(i_comand.config_export_sync(repo.pach))
    cast_cmd_list(conn, repo.get_commit_cmd(parser.args["text"][0]))
    cast_cmd_list(conn, repo.get_push_cmd())
