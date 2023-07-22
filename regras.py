#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" reg 'ras' after update version 1C"""
from utils_1c import settings_1c, connection_1c, argparse_1c


def status(cast):
    answ = cast('ps -C ras --format "pid"').split("\n")
    if len(answ) > 2:
        for k in range(1, len(answ) - 1):
            print("ras is running, PID: {}".format(answ[k]))
            return True
    else:
        print("ras is stopped")
        return False


def start(cast, platform="deb"):
    sets = settings_1c.Settings()
    print("starting ras")
    cast("{0} cluster --daemon".format(sets.ras_pach[platform]))


def stop(cast):
    print("stopping ras")
    answ = cast('ps -C ras --format "pid"').split("\n")
    if len(answ) > 2:
        for k in range(1, len(answ) - 1):
            cast('kill {0}'.format(answ[k]))


parser = argparse_1c.ArgumentParser_1C("Skf", description=__doc__)
parser.add_argument('-o', '--mode',
                    metavar="MODE",
                    help='start/stop/status/restart',
                    nargs="*", type=str, required=False)
parser.decode_arg()
for srv in parser.args["server"]:
    with connection_1c.Connection(srv=srv, **parser.args) as conn:
        if parser.args["mode"][0] == "status":
            status(conn.cast)
        elif parser.args["mode"][0] == "start":
            if not status(conn.cast):
                start(conn.cast, parser.args["platform"])
        elif parser.args["mode"][0] == "stop":
            stop(conn.cast)
        elif parser.args["mode"][0] == "restart":
            stop(conn.cast)
            start(conn.cast, parser.args["platform"])

