#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import basedata, connection_1c, argparse_1c, ocv8, rep, tw, server, sessionmanager, baselock


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
    answ = conn.cast("ps x | grep 1cv8 | grep {}".format(base)).split("\n")
    for k in range(0, len(answ) - 1):
        raise Exception("Base is locked by process: {}".format(k))

    ds_base = basedata.get_designer_base(**parser.get_single_base_params())
    repo = rep.Repository(parser.args["repozitory"][0])

    cv = ocv8.DesignerCommand(*ds_base.getparams(), "/UC {}".format("bkp_bot_key"), env="DISPLAY=:1",
                              cmd_func=conn.cast)
    cast_cmd_list(conn, repo.get_pull_cmd("origin master"))
    outlog = "/tmp/outlog_{}.log".format(base)
    conn.cast('[ -d "{0}" ] && rm -r {0}'.format(outlog))
    w = tw.ThreadWorker(cv.LoadConfigFromFilesUPD)
    if parser.args["dynamic"]:
        done = w.make_work((repo.pach, True, outlog), 1000)
    else:
        server1c = server.Server(cmd_func=conn.cast, **parser.args)
        sm = sessionmanager.SessionManager(server1c)
        cl_base = server1c.get_clbase(base_name=base, usr=parser.usr, pwd=parser.pwd, **parser.args)
        with baselock.BaseLock(cl_base, uc="bkp_bot_key", cmd_func=conn.cast) as bl:
            sm.terminate_all(base)
            done = w.make_work((repo.pach, False, outlog), 1000)
    if done:
        print(conn.cast('cat {}'.format(outlog)))
    else:
        answ = conn.cast("ps x | grep 1cv8 | grep {} | cut -d ' ' -f 1".format(base)).split("\n")
        for k in range(0, len(answ) - 1):
            conn.cast('kill {0}'.format(answ[k]))
        print("!!!ERROR update {}".format(base))
    conn.cast('rm {}'.format(outlog))
