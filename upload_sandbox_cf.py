#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""upload .cf from local to sandbox"""

from sets_1c import ibcmd
from sets_1c import settings_1c
from sets_1c import argparse_1c
import os

parser =argparse_1c.ArgumentParser_1C("sbk", description=__doc__)
parser.add_argument('-p', '--pach',
				metavar="PACH",
				help='local base pach',
				nargs=1,type=str, required=True)
parser.decode_arg()

cmdmn = ibcmd.IbCmd(
            lambda x: os.system(x),
            ibcmd.get_file_bparams(parser.args["pach"][0]),
            "deb", parser.args["test"])

fm = settings_1c.FileManager()
tmpf = fm.tmpf("/tmp", parser.b[0], "cf")

cmdmn.run(cmdmn.create_cmd("config save", tmpf))