#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import basedata, connection_1c, argparse_1c, infobase_comand, rep, ocv8


def cast_cmd_list(cn, cmd_list):
    for cm in cmd_list:
        print(cn.cast(cm))


parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.decode_arg()

srv = parser.args["server"][0]
base = parser.args["base"][0]
ds_base = basedata.get_designer_base(**parser.get_single_base_params())

with connection_1c.Connection(srv=srv, **parser.args) as conn:
    ibcmd_base = basedata.get_ibcmd_base(base=base, type="file", srv=srv,
                                         cat_pach=base,
                                         usr=parser.usr, pwd=parser.pwd,
                                         db_usr=parser.db_usr, db_pwd=parser.db_pwd)

    i_comand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                               cmd_func=conn.cast)
    cv = ocv8.DesignerCommand(*ds_base.getparams(),
                              "/UC {}".format("bkp_bot_key"),
                              env=ds_base.env,
                              cmd_func=conn.cast)

    repo = rep.Repository(parser)
    cast_cmd_list(conn, repo.get_start_reload_cmd())
    print(i_comand.config_reset())
    #print(i_comand.config_import(repo.pach))
    #print(i_comand.config_apply())
    conn.cast('[ -e "{0}" ] && rm -r {0}'.format(ds_base.outlog))
    cv.LoadConfigFromFilesUPD(repo.pach, True, ds_base.outlog)
    print(conn.cast("cat {0}".format(ds_base.outlog)))
    conn.cast('[ -e "{0}" ] && rm -r {0}'.format(ds_base.outlog))
    print(i_comand.config_export('/tmp/tmpxml'))
    cast_cmd_list(conn, repo.get_end_reload_cmd())
    print(i_comand.config_export_sync(repo.pach))
