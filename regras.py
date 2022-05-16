#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" reg 'ras' after update version 1C"""
from utils_1c import settings_1c, connection_1c, argparse_1c


def reg(cast, platform="deb"):
    sets = settings_1c.Settings()
    answ = cast('ps -C ras --format "pid"').split("\n")
    if len(answ) > 2:
        for k in range(1, len(answ) - 1):
            cast('kill {0}'.format(answ[k]))
    cast("{0} --daemon cluster".format(sets.ras_pach[platform]))


parser = argparse_1c.ArgumentParser_1C("Skf", description=__doc__)
parser.decode_arg()
for srv in parser.args["server"]:
    with connection_1c.Connection(srv=srv, **parser.args) as conn:
        reg(conn.cast, parser.args["platform"])
