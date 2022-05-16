#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import filestorage, connection_1c, argparse_1c

parser = argparse_1c.ArgumentParser_1C("sl", description=__doc__)
parser.add_argument('-o', '--o_pach',
                    metavar="O_PACH",
                    help='/var/lib/gtmms/data/AAAA/YYYYYY/XXXXXX/DPA_5.1.pdf',
                    nargs=1, type=str, required=True)
parser.decode_arg()

lst = filestorage.FileStorage(connection_1c.LocalConnection(), parser.args['gtmms'][0])

if lst.exists(parser.args['o_pach'][0]):
    print("ya")
else:
    with connection_1c.Connection(srv=parser.args["server"][0], **parser.args) as conn:
        rst = filestorage.FileStorage(conn, parser.args['pach'][0])
        rst.get(parser.args['o_pach'][0])
"""
with as conn:
    l
    print(lst.old_files())


    
    for file in lst.old_files(age=3):
        print(file)

    #pach = "/var/lib/gtmms/data/sales/2BtrackedBV/W3HE_1807-1_AA-2/DPA_5.1.pdf"
    #print(conn.stat(pach).st_mtime)  """
