#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


class BaseLock(object):

    """block base to make safe backup"""

    def __init__(self, server1c, base, usr, pwd):
        super(BaseLock, self).__init__()
        self.server = server1c
        self.base = base
        self.locked = False
        self.usr = usr
        self.pwd = pwd

    def __enter__(self):
        self.block()
        return self

    def __exit__(self, type1, value, traceback):
        self.unblock()

    def block(self):
        print(self.server.get_bases())
        return self.base
        #cmd = "infobase --cluster={cluster} update --infobase={infobase}"
        #cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
        #cmd = cmd + " --sessions-deny=on --scheduled-jobs-deny=on"
        #cmd = cmd + '--denied-message="backup in progress"'
        #cmd = cmd.format(**self.server.get_base(self.base))
        #self.server.run(cmd)
        #self.locked = True
        #return self

    def unblock(self):
            cmd = "infobase --cluster={cluster} update --infobase={infobase}"
            cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
            cmd = cmd + " --sessions-deny=off --scheduled-jobs-deny=off"
            cmd = cmd.format(**self.server.get_base(self.base))
            self.server.run(cmd)
            print(cmd)
            self.locked = False

    def runmethod(self, method):
        cmd_method = getattr(self, method)
        cmd_method()

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from sets_1c import argparse_1c
    from sets_1c import connection_1c
    from utils_1c import server

    parser = argparse_1c.ArgumentParser_1C("sbuk", description=__doc__)
    parser.add_argument('-m', '--method',
                        metavar="MTD",
                        help='block/unblock',
                        nargs=1, type=str, default="block", required=False)
    parser.add_argument('-f', '--platform',
                        metavar="DEB",
                        help='deb/win',
                        nargs=1, type=str, default="deb", required=False)

    parser.decode_arg()
    print("BaseLock: {}".format(parser.args["method"][0]))
    with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
        bl = BaseLock(server.Server(cmd_func=conn.cast,
                                    platform=parser.args["platform"]),
                                    parser.b[0], parser.usr, parser.pwd)
        bl.runmethod(parser.args["method"][0])

