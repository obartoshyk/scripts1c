#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from . import server, comand_1c, connection_1c, argparse_1c


class LockCommandMaker(object):
    def __init__(self, clbase):
        super(LockCommandMaker, self).__init__()
        self.cb = clbase

    def get_block(self):
        cmd = "infobase --cluster={}" \
              " update --infobase={}" \
              " --infobase-user={}" \
              " --infobase-pwd={}" \
              " --sessions-deny=on" \
              " --scheduled-jobs-deny=on" \
              ' --denied-message="denied by 1cbot"'
        return cmd.format(self.cb.cluster, self.cb.base, self.cb.usr, self.cb.pwd)

    def get_unblock(self):
        cmd = "infobase --cluster={}" \
              " update --infobase={}" \
              " --infobase-user={} " \
              "--infobase-pwd={}" \
              " --sessions-deny=off --scheduled-jobs-deny=off"
        return cmd.format(self.cb.cluster, self.cb.base, self.cb.usr, self.cb.pwd)


class BaseLock(comand_1c.CommandMaker):
    """block base to make safe backup"""

    def __init__(self, clbase, **kwargs):
        super(BaseLock, self).__init__()
        comand_1c.CommandMaker.__init__(self, command="rac", **kwargs)
        self.cmaker = LockCommandMaker(clbase)
        self.locked = False

    def __enter__(self):
        self.block()
        return self

    def __exit__(self, type1, value, traceback):
        if self.locked:
            self.unblock()

    def block(self):
        self.run(self.cmaker.get_block())
        self.locked = True
        return self.locked

    def unblock(self):
        self.run(self.cmaker.get_unblock())
        self.locked = False
        return self.locked

    def runmethod(self, method):
        cmd_method = getattr(self, method)
        cmd_method()


if __name__ == "__main__":

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

    with connection_1c.Connection(srv=parser.s[0], **parser.args) as conn:
        server1c = server.Server(cmd_func=conn.cast,
                                 platform=parser.args["platform"])
        bl = BaseLock(server1c.get_clbase(parser.b[0], parser.usr, parser.pwd),
                      cmd_func=conn.cast)
        bl.runmethod(parser.args["method"][0])
