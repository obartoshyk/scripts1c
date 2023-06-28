#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import basedata, connection_1c, argparse_1c, infobase_comand, rep
from utils_1c import ocv8


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

ds_base = basedata.get_designer_base(**parser.get_single_base_params())
ibcmd_base = basedata.get_ibcmd_base(base=base, type="file", srv=srv,
                                     cat_pach=base,
                                     usr=parser.usr, pwd=parser.pwd,
                                     db_usr=parser.db_usr, db_pwd=parser.db_pwd)

with connection_1c.Connection(srv=srv, **parser.args) as conn:
    i_comand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                               cmd_func=conn.cast)
    repo = rep.RepositoryPlugins(parser, conn)

    print(i_comand.config_export_sync(repo.pach))
    dc = ocv8.DesignerCommand(*ds_base.getparams(),
                              cmd_func=conn.cast,
                              env=parser.args["env"][0])
    repo.initialise_export()
    dc.convert_plugins(repo)
    cast_cmd_list(conn, repo.get_commit_cmd(parser.args["text"][0]))
    cast_cmd_list(conn, repo.get_push_cmd())
