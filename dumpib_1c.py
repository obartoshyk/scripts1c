#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, settings_1c
from utils_1c import sessionmanager, baselock, server, basedata, infobase_comand, connection_1c

parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='backup cat pach',
                    nargs="*", type=str, required=False)
parser.decode_arg()

fm = settings_1c.FileManager()
fm.init_bkp_pach(parser.args["pach"][0])
srv = parser.s[0]
print("***{} starting backup {}".format(settings_1c.str_cur_time(), srv))
with connection_1c.Connection(srv=srv, **parser.args) as conn:
    server1c = server.Server(cmd_func=conn.cast, **parser.args)
    sm = sessionmanager.SessionManager(server1c)

    for base_name in parser.b:
        ibcmd_base = basedata.IbcmdPostgresBase(
            srv=srv,
            base=base_name,
            usr=parser.usr, pwd=parser.pwd,
            db_usr=parser.db_usr,
            db_pwd=parser.db_pwd)

        cl_base = server1c.get_clbase(base_name=base_name, usr=parser.usr, pwd=parser.pwd, **parser.args)



        icomand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                                  cmd_func=conn.cast,
                                                  platform=parser.args["platform"])

        tmp_dt = fm.tmp_bkp_filename(base_name, "dt")
        dest_dt = fm.dest_bkp_filename(base_name, "dt")

        print("***{} starting dump {}".format(settings_1c.str_cur_time(), base_name))
        sm.terminate_all(base_name)
        with baselock.BaseLock(cl_base, cmd_func=conn.cast) as bl:

            print(icomand.dump(tmp_dt))

            conn.cast("chmod a+r " + tmp_dt)
            conn.move_file(tmp_dt, dest_dt)

        print("***{} finished dump {}".format(settings_1c.str_cur_time(), base_name))

print("***{} finished backup {}".format(settings_1c.str_cur_time(), srv))
