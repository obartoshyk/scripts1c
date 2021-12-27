#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import connection_1c, argparse_1c, server, sessionmanager

parser = argparse_1c.ArgumentParser_1C("sBudkf", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='backup cat pach',
                    nargs="*", type=str, required=False)
parser.decode_arg()
