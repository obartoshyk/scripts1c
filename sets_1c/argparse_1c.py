#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# import subprocess
import argparse


class ArgumentParser_1C(argparse.ArgumentParser):
    """argparse for 1C skripts"""

    def __init__(self, modeline="", **kwargs):
        super(ArgumentParser_1C, self).__init__(**kwargs)
        self.add_argument('-t', '--test', help='Test mode', action='store_true', default=False)
        self.add_argument('-cfg', '--cfg_file', help='cfg file pach', required=False)
        self.modeline = modeline
        self.add_b()
        self.add_s()
        self.add_c()
        self.add_user()
        self.add_d()
        self.add_k()
        self.args = {}

    def decode_arg(self):
        args = vars(self.parse_args())
        for k, v in args.items():
            self.args[k] = v
        cfg_file = self.args.get("cfg_file")
        if cfg_file:
            self.decode_cfg(cfg_file)
        self.decode_args(args)
        return args

    def decode_args(self, args):
        self.decode_b(args)
        self.decode_s(args)
        self.decode_c(args)
        self.decode_u(args)
        self.decode_d(args)

    def add_b(self):
        if self.modeline.find("b") != -1:
            self.add_argument('-b', '--base',
                              metavar="BASE",
                              help='1C Base',
                              nargs=1, type=str, required=False)
        if self.modeline.find("B") != -1:
            self.add_argument('-b', '--base',
                              metavar="BASES",
                              help='1C Bases list',
                              nargs="*", type=str,
                              required=False)

    def add_s(self):
        if self.modeline.find("s") != -1:
            self.add_argument('-s', '--server',
                              metavar="SRV",
                              help='1C Server',
                              nargs=1, type=str, required=False)
        if self.modeline.find("S") != -1:
            self.add_argument('-s', '--server',
                              metavar="SRVS",
                              help='1C Server list',
                              nargs="*", type=str,
                              required=False)

    def add_c(self):
        if self.modeline.find("c") != -1:
            self.add_argument('-c', '--client',
                              metavar="CLIENT",
                              help='1C Client',
                              nargs=1, type=str, required=False)
        if self.modeline.find("C") != -1:
            self.add_argument('-c', '--client',
                              metavar="CLIENTS",
                              help='1C Clients list(empty=ALL)',
                              nargs="*", type=str,
                              required=False)

    def add_user(self):
        if self.modeline.find("u") != -1:
            self.add_argument('-u', '--user',
                              metavar="user:login",
                              help='1c base user',
                              nargs=1, type=str, required=False)

    def add_d(self):
        if self.modeline.find("d") != -1:
            self.add_argument('-d', '--db_user',
                              metavar="user:login",
                              help='SQL base user',
                              nargs=1, type=str, required=False)

    def add_k(self):
        if self.modeline.find("k") != -1:
            self.add_argument('-k', '--ssh_key',
                              metavar="~pach/.ssh/id_rsa",
                              help='rsa key to ssh connection',
                              nargs=1, type=str, required=False)
        if self.modeline.find("K") != -1:
            self.add_argument('-k', '--ssh_key',
                              metavar="~pach/.ssh/id_rsa",
                              help='rsa key to ssh connection',
                              nargs=1, type=str, required=False)

    def decode_b(self, args):
        if self.modeline.find("b") != -1:
            self.b = args["base"]
        if self.modeline.find("B") != -1:
            self.b = args["base"]

    def decode_c(self, args):
        if self.modeline.find("c") != -1:
            self.c = args["client"]
        if self.modeline.find("C") != -1:
            self.c = args["client"]

    def decode_s(self, args):
        if self.modeline.find("s") != -1:
            self.s = args["server"]
        if self.modeline.find("S") != -1:
            self.s = args["server"]

    def decode_u(self, args):
        if self.modeline.find("u") != -1:
            self.usr, self.pwd = args['user'][0].split(":")

    def decode_d(self, args):
        if self.modeline.find("d") != -1:
            self.db_usr, self.db_pwd = args['db_user'][0].split(":")

    def decode_cfg(self, cfg_file):
        with open(cfg_file, 'r') as cfile:
            for line in cfile.read().splitlines():
              print(line)


if __name__ == "__main__":
    parser = ArgumentParser_1C("s", description=__doc__)
    print(parser.decode_arg())
