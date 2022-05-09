#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import argparse_1c, connection_1c, xvfb


parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-o', '--mode',
                    metavar="MODE",
                    help='start/stop/status/restart',
                    nargs="*", type=str, required=False)
parser.decode_arg()
with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
    x = xvfb.Xvfb(conn)
    if parser.args["mode"][0] == "status":
        status = x.status()
        if status:
            print("Xvfb running, PID: {}".format(status))
        else:
            print("Xvfb stopped")
    elif parser.args["mode"][0] == "start":
        print(x.start())
    elif parser.args["mode"][0] == "stop":
        print(x.stop())
    elif parser.args["mode"][0] == "restart":
        print(x.restart())
