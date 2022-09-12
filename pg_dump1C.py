#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, settings_1c
from utils_1c import server, connection_1c
from utils_1c import tw


class DumpMaker(object):
    def __init__(self):
        super(DumpMaker, self).__init__()
        self.conn = None
        self.base_name = None
        self.server1c = None
        self.cl_base = None
        self.parser = None
        self.fm = None
        self.srv = None
        self.ds_base = None

    def init_parser(self, parser_obj):
        self.parser = parser_obj
        self.fm = settings_1c.FileManager()
        self.fm.init_bkp_pach(self.parser.args["pach"][0])
        self.srv = self.parser.args["server"][0]

    def make_single_dump(self):

        self.conn.cast("/etc/init.d/srv1cv83 stop")
        dest_dt = self.fm.dest_bkp_filename(self.base_name, "dt")
        tmp_dt = dest_dt if connection_1c.localhost(self.srv) else self.fm.tmp_bkp_filename(self.base_name, "dt")

        cmd = "pg_dump --username={db_user} --no-password --file={tmp_dt} {base_name}"
        w = tw.ThreadWorker(self.conn.cast)
        dmp_status = w.make_work((cmd.format(self.parser.db_user, tmp_dt, self.base_name)), 7200)
        if dmp_status:
            print(w.get_data())
            self.conn.cast("chmod a+r " + tmp_dt)
            if tmp_dt != dest_dt:
                self.conn.move_file(tmp_dt, dest_dt)
        else:
            print("Backup of {} IS FAILED, restore base work!".format(self.base_name))
        self.conn.cast("/etc/init.d/srv1cv83 start")
        return dmp_status

    def init_connection(self, conn_id):
        self.conn = conn_id
        self.server1c = server.Server(cmd_func=self.conn.cast, **self.parser.args)

    def init_base(self, base_name_id):
        self.base_name = base_name_id
        self.cl_base = self.server1c.get_clbase(base_name=base_name_id,
                                                usr=self.parser.usr,
                                                pwd=self.parser.pwd,
                                                **self.parser.args)

    def make_dump(self):
        print("***{} starting backup {}".format(settings_1c.str_cur_time(), self.srv))
        with connection_1c.Connection(srv=self.srv, **self.parser.args) as conn:
            self.init_connection(conn)
            for base_name in self.parser.args["base"]:
                self.init_base(base_name)

                print("***{} starting dump {}".format(settings_1c.str_cur_time(), self.base_name))
                dmp_status = "Finished" if self.make_single_dump() else "FAILED"
                print("***{} {} dump {}".format(settings_1c.str_cur_time(), dmp_status, self.base_name))

        print("***{} finished backup {}".format(settings_1c.str_cur_time(), self.srv))


if __name__ == "__main__":
    parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
    parser.add_argument('-p', '--pach',
                        metavar="PACH",
                        help='backup cat pach',
                        nargs="*", type=str, required=False)
    parser.decode_arg()
    dp = DumpMaker()
    dp.init_parser(parser)
    dp.make_dump()
