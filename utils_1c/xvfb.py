#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
class Xvfb(object):
    def __init__(self, conn):
        super(Xvfb, self).__init__()
        self.conn = conn

    def start(self):
        return self.conn.cast("nohup Xvfb :1 -screen 0 1280x1024x24 -fbdir /var/tmp > /dev/null 2>&1 &")

    def stop(self):
        return self.conn.kill(self.status())

    def status(self):
        proc = self.conn.ps_grep(["Xvfb"])
        if proc:
            return proc[0]
        return ""

    def restart(self):
        if self.status():
            self.stop()
        return self.start()



