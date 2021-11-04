#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, settings_1c
from utils_1c import sessionmanager, baselock, server, basedata, comand_1c, connection_1c

parser = argparse_1c.ArgumentParser_1C("sBudk", description=__doc__)
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

    for base in parser.b:
        remote_base = basedata.IbcmdPostgresBase(
            srv=srv,
            base=base,
            db_usr=parser.db_usr,
            db_pwd=parser.db_pwd)

        tmp_dt = fm.tmp_bkp_filename(base, "dt")
        dest_dt = fm.dest_bkp_filename(base, "dt")

        print("***{} starting dump {}".format(settings_1c.str_cur_time(), base))
        sm.terminate_all(base)

        with baselock.BaseLock(server1c.get_clbase(parser.b[0], parser.usr, parser.pwd),
                               cmd_func=conn.cast) as bl:

            ibcmd = comand_1c.CommandMaker(*remote_base.getparams(), cmd_func=conn.cast)
            print(ibcmd.run("infobase dump", tmp_dt))

            conn.cast("chmod a+r " + tmp_dt)
            ftp = conn.ssh.open_sftp()
            ftp.get(tmp_dt, dest_dt)
            ftp.remove(tmp_dt)
            if ftp:
                ftp.close()

        print("***{} finished dump {}".format(settings_1c.str_cur_time(), base))

print("***{} finished backup {}".format(settings_1c.str_cur_time(), srv))
