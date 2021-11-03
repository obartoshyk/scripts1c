#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
class SessionManager(object):
    """terminate base or server sessions"""

    def __init__(self, server1c):
        super(SessionManager, self).__init__()
        self.server = server1c

    def current_sessions(self, base):
        cmd = "session --cluster={cluster} list --infobase={infobase}"
        cmd = cmd.format(**self.server.get_base(base))
        return self.server.takekeys(self.server.run(cmd))

    def terminate_session(self, cluster, session):
        cmd = "session --cluster={0} terminate --session={1}"
        cmd = cmd.format(cluster, session)
        self.server.run(cmd)

    def terminate_all(self, base):
        cluster = self.server.get_base(base)["cluster"]
        for curr_sess in self.current_sessions(base):
            self.terminate_session(cluster, curr_sess["session"])

    def terminate_sessions(self, base, userlist):
        cluster = self.server.get_base(base)["cluster"]
        for curr_sess in self.current_sessions(base):
            if curr_sess["user-name"] in userlist:
                self.terminate_session(cluster, curr_sess["session"])


if __name__ == "__main__":
    def terminate(smanager, b, c):
        for base in (b if b else smanager.server.get_bases().keys()):
            if c:
                smanager.terminate_sessions(base, c)
            else:
                smanager.terminate_all(base)

    import os
    import sys
    import server
    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    from sets_1c import argparse_1c

    parser = argparse_1c.ArgumentParser_1C("SBCk", description=__doc__)
    parser.add_argument('-f', '--platform',
                        metavar="DEB",
                        help='deb/win',
                        nargs=1, type=str, default="deb", required=False)
    parser.decode_arg()
    if not (parser.args["base"]) and not (parser.args["client"]):
        raise "I can`t ruin everything again!"
    if parser.s[0] == "localhost":
        if parser.args["test"]:
            def cmd_func(x): print(x)
        else:
            def cmd_func(x): return os.popen(x).read()
        sm = SessionManager(server.Server(
            cmd_func=cmd_func,
            platform=parser.args["platform"]))
        terminate(sm, parser.b, parser.c)
    else:
        from sets_1c import connection_1c
        for srv in parser.s:
            with connection_1c.Connection(srv=srv, **parser.args) as conn:
                if parser.args["test"]:
                    def cmd_func(x):
                        print(x)
                else:
                    def cmd_func(x):
                        return conn.cast(x)
                sm = SessionManager(server.Server(
                    cmd_func=cmd_func,
                    platform=parser.args["platform"]))
                terminate(sm, parser.b, parser.c)
