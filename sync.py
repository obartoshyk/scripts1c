#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from utils_1c import localfilestorage, argparse_1c
import threading


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts] for i in range(wanted_parts)]


def make_lst(p, trn):
    return localfilestorage.FileStorage(srv=p.args["server"][0],
                                        storage_path=p.args['gtmms'][0],
                                        trn=trn,
                                        **p.args)


def sync_export(trn, p, old_f):
    lse = make_lst(p, str(trn))
    lse.sync_export(old_f)


def sync_import(trn, p, emp=""):
    lse = make_lst(p, str(trn))
    lse.sync_import()


def sync_remove(trn, p, emp=""):
    lse = make_lst(p, str(trn))
    lse.sync_remove()


def tr(func, count, p):
    threads = []
    counter = 0
    for fl in count:
        t = threading.Thread(target=func, args=(counter, p, fl))
        threads.append(t)
        t.start()
        counter += 1
    for t in threads:
        t.join()


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
lst = make_lst(parser, "")

if parser.args['mode'][0] == "export":
    age = int(parser.args['time'][0]) if int(parser.args['time'][0]) > 100 else 365
    old_files = lst.old_files(age=age)
    arr_list = split_list(old_files, lst.get_export_stream_counter(old_files))
    tr(sync_export, arr_list, parser)

elif parser.args['mode'][0] == "import":
    stk = lst.get_import_stream_counter()
    if stk >= 0:
        tr(sync_import, range(stk), parser)

elif parser.args['mode'][0] == "remove":
    stk = lst.get_import_stream_counter()
    if stk >= 0:
        tr(sync_remove, range(stk), parser)

