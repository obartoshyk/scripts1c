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
        return self.server.run(cmd)

    def terminate_all(self, base):
        answ = []
        cluster = self.server.get_base(base)["cluster"]
        for curr_sess in self.current_sessions(base):
            answ.append(self.terminate_session(cluster, curr_sess["session"]))
        return answ

    def terminate_sessions(self, base, user_list):
        answ = []
        cluster = self.server.get_base(base)["cluster"]
        for curr_sess in self.current_sessions(base):
            if curr_sess["user-name"] in user_list:
                answ.append(self.terminate_session(cluster, curr_sess["session"]))
        return answ
