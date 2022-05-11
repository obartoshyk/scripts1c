#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import filestorage, connection_1c, argparse_1c


def sync(file_pach, local_storage, remote_storage):
    remote_storage.put(file_pach)
    print(local_storage.rm(file_pach))


parser = argparse_1c.ArgumentParser_1C("s", description=__doc__)
parser.add_argument('-p', '--pach',
                    metavar="PACH",
                    help='/var/lib/gtmms/data/sales',
                    nargs=1, type=str, required=True)
parser.add_argument('-o', '--time',
                    metavar="TIME",
                    help='1-20',
                    nargs=1, type=str, required=True)
parser.decode_arg()

lst = filestorage.FileStorage(connection_1c.LocalConnection(), parser.args['pach'][0])

with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
    rst = filestorage.FileStorage(conn, parser.args['pach'][0])
    for file in lst.old_files(age=int(parser.args['time'][0])):
        sync(file, lst, rst)
