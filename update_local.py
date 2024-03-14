#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import basedata, connection_1c, argparse_1c, ocv8, rep, tw, server, sessionmanager, baselock
from time import sleep


def cast_cmd_list(cn, cmd_list):
    for cm in cmd_list:
        print(cn.cast(cm))


parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-i', '--dynamic',
                    action='store_true',
                    help='dynamic 1C mode',
                    default=False)
parser.decode_arg()

srv = parser.args["server"][0]
base = parser.args["base"][0]

with connection_1c.Connection(srv=srv, **parser.args) as conn:

    ds_base = basedata.get_designer_base(**parser.get_single_base_params())
    repo = rep.Repository(parser)
    cast_cmd_list(conn, repo.get_pull_cmd("origin master"))
    cv = ocv8.DesignerCommand(*ds_base.getparams(),
                              "/UC {}".format("bkp_bot_key"),
                              env=ds_base.env,
                              cmd_func=conn.cast)

    conn.cast('[ -e "{0}" ] && rm -r {0}'.format(ds_base.outlog))
    try:
        dynamic = parser.args["dynamic"]
    except:
        dynamic = False
    cv.LoadConfigFromFilesUPD(repo.pach, dynamic, ds_base.outlog)
    conn.cast("cat {0}".format(ds_base.outlog))
    conn.cast('[ -e "{0}" ] && rm -r {0}'.format(ds_base.outlog))
