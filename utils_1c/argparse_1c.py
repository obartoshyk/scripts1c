#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import argparse
import yaml


class ArgumentParser_1C(argparse.ArgumentParser):
    """argparse for 1C skripts"""

    def __init__(self, modeline="", **kwargs):
        super(ArgumentParser_1C, self).__init__(**kwargs)
        self.add_argument('-t', '--test', help='Test mode', action='store_true', default=False)
        self.add_argument('-y', '--yaml_file', help='.yml file pach', required=False)
        self.modeline = modeline
        self.args = {"test": False}
        self.add_base()
        self.add_server()
        self.add_client()
        self.add_user()
        self.add_d()
        self.add_k()
        self.add_platform()
        self.add_gtmms()

    def decode_arg(self):
        args = vars(self.parse_args())
        yaml_file = args.get("yaml_file")
        if yaml_file:
            self.decode_yaml(yaml_file)
        for k, v in args.items():
            if v:
                self.args[k] = v

        self.decode_special_args()
        return self.args

    def decode_special_args(self):
        for k, v in self.args.items():
            if k == "user":
                self.usr, self.pwd = self.args['user'][0].split(":")
                if self.pwd == "NONE":
                    self.pwd = ""
            if k == "db_user":
                self.db_usr, self.db_pwd = self.args['db_user'][0].split(":")
                if self.db_pwd == "NONE":
                    self.db_pwd = ""
            if k == "ssh_key" or k == "type":
                if self.args[k]:
                    self.args[k] = self.args[k][0]

    def add_platform(self):
        if self.modeline.find("f") != -1:
            self.args["platform"] = "deb"
            self.add_argument('-f', '--platform',
                              metavar="DEB",
                              help='deb/win',
                              nargs=1, type=str, default="deb", required=False)

    def add_base(self):
        if self.modeline.find("b") != -1 or self.modeline.find("B") != -1:
            self.add_argument('-b', '--base',
                              metavar="BASES",
                              help='1C Bases list',
                              nargs="*", type=str,
                              required=False)

    def add_server(self):
        if self.modeline.find("s") != -1 or self.modeline.find("S") != -1:
            self.add_argument('-s', '--server',
                              metavar="SRVS",
                              help='1C Server list',
                              nargs="*", type=str,
                              required=False)

    def add_gtmms(self):
        if self.modeline.find("l") != -1 or self.modeline.find("L") != -1:
            self.add_argument('-l', '--gtmms',
                              metavar="BASES",
                              help='1C file storage path',
                              nargs="*", type=str,
                              required=False)

    def add_client(self):
        if self.modeline.find("c") != -1 or self.modeline.find("C") != -1:
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
        if self.modeline.find("k") != -1 or self.modeline.find("K") != -1:
            self.add_argument('-k', '--ssh_key',
                              metavar="~pach/.ssh/id_rsa",
                              help='rsa key to ssh connection',
                              nargs=1, type=str, required=False)

    def decode_yaml(self, cfg_file):
        with open(cfg_file, 'r') as stream:
            for k, i in yaml.safe_load(stream).items():
                self.args[k] = i

    def get_single_base_params(self):
        pl = ["srv", "server", "base",
              "usr", "pwd", "db_usr", "db_pwd",
              "type", "cat_pach", "gtmms"]
        sb_params = {atr: getattr(self, atr) for atr in pl if hasattr(self, atr)}
        for k, v in self.args.items():
            if k in pl:
                sb_params[k] = v
        for k, v in sb_params.items():
            if isinstance(v, list):
                sb_params[k] = v[0]
        return sb_params


if __name__ == "__main__":
    parser = ArgumentParser_1C("s", description=__doc__)
    print(parser.decode_arg())
