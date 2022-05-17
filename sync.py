#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import localfilestorage, argparse_1c


parser = argparse_1c.ArgumentParser_1C("sk", description=__doc__)
parser.add_argument('-o', '--time',
                    metavar="TIME",
                    help='1-20',
                    nargs=1, type=str, required=True)
parser.add_argument('-m', '--mode',
                    metavar="MODE",
                    help='export/import',
                    nargs="*", type=str, required=True)
parser.decode_arg()
lst = localfilestorage.FileStorage(srv=parser.args["server"][0],
                                   storage_path=parser.args['gtmms'][0],
                                   **parser.args)

if parser.args['mode'][0] == "export":
    lst.sync_export(age=int(parser.args['time'][0]))
elif parser.args['mode'][0] == "import":
    lst.sync_import()




