#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import server, connection_1c, argparse_1c, baselock


def run_method(locker, method):
    cmd_method = getattr(locker, method)
    cmd_method()


parser = argparse_1c.ArgumentParser_1C("sbukf", description=__doc__)
parser.add_argument('-m', '--method',
                    metavar="MTD",
                    help='block/unblock',
                    nargs=1, type=str, default="block", required=False)
parser.decode_arg()

for srv in parser.args["server"]:
    with connection_1c.Connection(srv=srv, **parser.args) as conn:
        server1c = server.Server(cmd_func=conn.cast,
                                 platform=parser.args["platform"])
        for base_name in server1c.get_bases() if not parser.args["base"] else parser.args["base"]:
            cl_base = server1c.get_clbase(base_name=base_name,
                                          usr=parser.usr,
                                          pwd=parser.pwd,
                                          **parser.args)
            bl = baselock.BaseLock(cl_base, cmd_func=conn.cast, uc="bkp_bot_key")
            run_method(bl, parser.args["method"][0])
