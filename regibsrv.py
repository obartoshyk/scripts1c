#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" 
reg ibsrv daemon from conf on remote server
"""
from sets_1c import settings_1c, connection_1c, argparse_1c
import os
import time


def ibsrv_start_cmd(pach, c_file):
    return '{ibsrv_pach} \
        -c 	"{pach}/conf/{basename}.yaml"  \
        --data "{pach}/{basename}_wdr"  \
        --daemon'.format(
        ibsrv_pach=settings_1c.Settings().ibsrv_pach["deb"],
        pach=pach,
        basename=c_file.replace(".yaml", ""))


def ibsrv_start_cmd_list(pach, source):
    return [ibsrv_start_cmd(pach, c_) for c_ in source.listdir("{0}/conf".format(pach))]


def kill_list(answer):
    if len(answer) > 2:
        return ['kill -9 {0}'.format(answer[k]) for k in range(1, len(answer) - 1)]
    else:
        return []


def remote_run(cmd_list, conn):
    for cmd in cmd_list:
        conn.cast(cmd) if not conn.testmode else print(cmd)


def local_run(cmd_list, test_mode):
    for cmd in cmd_list:
        print("run: {}".format(cmd))
        if not test_mode:
            os.system(cmd)


def remote(prs):
    with connection_1c.Connection(srv=prs.s[0], **prs.args) as conn:
        answer = conn.cast('ps -C ibsrv --format "pid"').split("\n")
        remote_run(kill_list(answer), conn)
        time.sleep(5)
        ftp = conn.ssh.open_sftp()
        if ftp:
            remote_run(ibsrv_start_cmd_list(prs.args["pach"][0], ftp), conn)
            ftp.close()


def local(prs):
    answer = os.popen('ps -C ibsrv --format "pid"').read().split("\n")
    local_run(kill_list(answer), prs.args["test"])
    time.sleep(5)
    local_run(ibsrv_start_cmd_list(prs.args["pach"][0], os), prs.args["test"])


if __name__ == "__main__":
    parser = argparse_1c.ArgumentParser_1C("sk", description=__doc__)
    parser.add_argument('-p', '--pach',
                        metavar="pach",
                        help='ibsrv conf pach',
                        nargs=1, type=str, required=True)
    parser.decode_arg()
    local(parser) if parser.s[0] == "localhost" else remote(parser)
