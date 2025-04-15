#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" config reset : reset base config to default
"""

from utils_1c import basedata, connection_1c, argparse_1c, infobase_comand

parser = argparse_1c.ArgumentParser_1C("sbkduf", description=__doc__)
parser.decode_arg()

for srv_name in parser.args["server"]:
    with connection_1c.Connection(srv=srv_name, **parser.args) as conn:
        for base_name in parser.args["base"]:
            ibcmd_base = basedata.get_ibcmd_base(base=base_name, type="file", srv=srv_name,
                                                 cat_pach=base_name,
                                                 usr=parser.usr, pwd=parser.pwd,
                                                 db_usr=parser.db_usr, db_pwd=parser.db_pwd)
            i_comand = infobase_comand.InfobaseCommand(*ibcmd_base.getparams(),
                                                       cmd_func=conn.cast)
            print(i_comand.config_reset())