#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" 
reg ibsrv daemon from conf on remote server
usage:
   mode : start / stop / restart
   base : basename / all
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


def kill_list(answer, base):
    kill_l = []
    for ans_str in answer:
        if ans_str.find("grep") == -1 and (base == "all" or ans_str.find("{0}_wdr".format(base)) != -1):
            l_ans = list(filter(lambda x: True if x else False, ans_str.split(" ")))
            if len(l_ans) > 2:
                kill_l.append('kill -9 {0}'.format(l_ans[1]))
    return kill_l


class IbSrv(object):
    """ IbSrv server utils"""

    def __init__(self, mode="restart", base="all", pach="", test=True):
        super(IbSrv, self).__init__()
        self.test = test
        self.mode = mode
        self.base = base
        self.pach = pach

    def cmd_run(self, cmd_func, cmd_list):
        for cmd in cmd_list:
            print("run: {}".format(cmd))
            if not self.test:
                cmd_func(cmd)

    def local(self):
        if self.mode != "start":
            cmdline = self.local_remote_kill_list(lambda x: os.popen(x).read())
            self.cmd_run(lambda x: os.system(x), cmdline)
            if not self.test:
                time.sleep(5)
        if self.mode != "stop":
            cmdline = self.local_remote_start_list(os)
            self.cmd_run(lambda x: os.system(x), cmdline)

    def local_remote_kill_list(self, find_cmd):
        answer = find_cmd('ps aux | grep ibsrv').split("\n")
        return kill_list(answer, self.base)

    def local_remote_start_list(self, source):
        if self.base == "all":
            cmdlist = ibsrv_start_cmd_list(self.pach, source)
        else:
            cmdlist = [ibsrv_start_cmd(self.pach, self.base)]
        return cmdlist

    def remote(self, con):
        if self.mode != "start":
            cmdlist = self.local_remote_kill_list(lambda x: con.cast(x))
            self.cmd_run(lambda x: con.cast(x), cmdlist)
            if not self.test:
                time.sleep(5)
        if self.mode != "stop":
            ftp = con.ssh.open_sftp()
            if ftp:
                cmdlist = self.local_remote_start_list(ftp)
                self.cmd_run(lambda x: con.cast(x), cmdlist)
                ftp.close()


if __name__ == "__main__":
    parser = argparse_1c.ArgumentParser_1C("skb", description=__doc__)
    parser.add_argument('-p', '--pach',
                        metavar="pach",
                        help='ibsrv conf pach',
                        nargs=1, type=str, required=True)
    parser.add_argument('-m', '--mode',
                        metavar="mode",
                        help='mode: start/stop/restart',
                        nargs=1, type=str, required=True)

    parser.decode_arg()
    params = {"mode": parser.args["mode"][0],
              "base": parser.args["base"][0],
              "pach": parser.args["pach"][0],
              "test": parser.args["test"]}

    oIbSrv = IbSrv(**params)

    if parser.s[0] == "localhost":
        oIbSrv.local()
    else:
        with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
            oIbSrv.remote(conn)
