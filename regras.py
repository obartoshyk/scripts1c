#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" reg 'ras' after update version 1C"""
from sets_1c import settings_1c, connection_1c, argparse_1c


def reg(cast, platform):
    sets = settings_1c.Settings()
    answ = cast('ps -C ras --format "pid"').split("\n")
    if len(answ) > 2:
        for k in range(1, len(answ) - 1):
            cast('kill{0}'.format(answ[k]))
    cast("{0} --daemon cluster".format(sets.ras_pach[platform]))


if __name__ == "__main__":
    parser = argparse_1c.ArgumentParser_1C("Sk", description=__doc__)
    parser.add_argument('-f', "--platform",
                        metavar="DEB",
                        help='deb/win',
                        nargs=1, type=str, default="deb", required=False)
    parser.decode_arg()
    for srv in parser.s:
        with connection_1c.Connection(srv=srv, **parser.args) as conn:
            if parser.args["test"]:
                def cmd_func(x):
                    print(x)
            else:
                def cmd_func(x):
                    conn.cast(x)
    reg(cmd_func, parser.args["platform"])
