#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
'''Upload external report from xml'''
from utils_1c import argparse_1c
from utils_1c import basedata, connection_1c, rep
from utils_1c import ocv8


def arg_parser_main():
    parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
    parser.decode_arg()
    return parser


if __name__ == "__main__":
    parser = arg_parser_main()
    ds_base = basedata.get_designer_base(**parser.get_single_base_params())
    with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
        dc = ocv8.DesignerCommand(*ds_base.getparams(),
                                  cmd_func=conn.cast,
                                  env=parser.args["env"][0])

        rp = rep.RepositoryPlugins(parser, conn)
        rp.initialise_export()
        rp.initialise_import()
        dc.convert_plugins(rp)
        rp.clear_export()

        #print(rp.exp)
        #print(rp.commits)
        #print(rp.imp)
