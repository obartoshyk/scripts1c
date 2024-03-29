#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import localfilestorage, argparse_1c
import urllib.parse
import os

parser = argparse_1c.ArgumentParser_1C("sl", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="O_PACH",
                    help='/var/lib/gtmms/data/AAAA/YYYYYY/XXXXXX/DPA_5.1.pdf',
                    nargs=1, type=str, required=True)
parser.decode_arg()

df_pach = urllib.parse.unquote_plus(parser.args['pach'][0])
if not os.path.exists(df_pach):
    localfilestorage.FileStorage(srv=parser.args["server"][0],
                                 storage_path=parser.args['gtmms'][0],
                                 trn=0,
                                 **parser.args).get(df_pach)
