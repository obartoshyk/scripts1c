#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, settings_1c
from utils_1c import sessionmanager, baselock, server, basedata,  connection_1c
from utils_1c import ocv8
import socket

parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='backup cat pach',
                    nargs="*", type=str, required=False)
parser.decode_arg()

fm = settings_1c.FileManager()
fm.init_bkp_pach(parser.args["pach"][0])
srv = parser.args["server"][0]
print("***{} starting backup {}".format(settings_1c.str_cur_time(), srv))
with connection_1c.Connection(srv=srv, **parser.args) as conn:
    server1c = server.Server(cmd_func=conn.cast, **parser.args)
    sm = sessionmanager.SessionManager(server1c)
    server1c.init_clusters()
    server1c.init_bases()
    for base_name in parser.args["base"]:
        ibcmd_base = basedata.IbcmdPostgresBase(
            srv=srv,
            base=base_name,
            usr=parser.usr, pwd=parser.pwd,
            db_usr=parser.db_usr,
            db_pwd=parser.db_pwd)

        cl_base = server1c.get_clbase(base_name=base_name, usr=parser.usr, pwd=parser.pwd, **parser.args)

        #icomand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
        #                                          cmd_func=conn.cast,
        #                                          platform=parser.args["platform"])

        ds_base = basedata.get_designer_base(**parser.get_single_base_params())

        tmp_dt = fm.tmp_bkp_filename(base_name, "dt")
        dest_dt = fm.dest_bkp_filename(base_name, "dt")
        if srv == "localhost" or srv == socket.gethostname():
            tmp_dt = dest_dt
        print("***{} starting dump {}".format(settings_1c.str_cur_time(), base_name))
        sm.terminate_all(base_name)

        with baselock.BaseLock(cl_base, uc="bkp_bot_key", cmd_func=conn.cast) as bl:

            cv = ocv8.DesignerCommand(*ds_base.getparams(), "/UC {}".format("bkp_bot_key"), env="DISPLAY=:1", cmd_func=conn.cast)
            print(cv.DumpIB(tmp_dt))

            conn.cast("chmod a+r " + tmp_dt)
            if tmp_dt != dest_dt:
                conn.move_file(tmp_dt, dest_dt)

        print("***{} finished dump {}".format(settings_1c.str_cur_time(), base_name))

print("***{} finished backup {}".format(settings_1c.str_cur_time(), srv))
