#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import paramiko
import socket
import os
from . import settings_1c


class RemoteConnection(object):
    """ Connection to 1C servers uses paramiko"""

    def __init__(self, srv="", ssh_key="", test=False, **kwargs):
        super(RemoteConnection, self).__init__()
        sets = settings_1c.Settings()
        self.testmode = test
        self.srv = srv
        self.ssh_key = ssh_key
        self.connected = False
        self.init_ras = False
        self.err = ""

        self.rac_pach = sets.rac_pach["deb"]
        self.ras_pach = sets.ras_pach["deb"]
        self.ibcmd_pach = sets.ibcmd_pach["deb"]
        self.ibsrv_pach = sets.ibsrv_pach["deb"]

        self.clusters_list = []
        self.bases_dict = {}
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        self.ssh.connect(hostname=self.srv, username='root', key_filename=self.ssh_key)
        self.connected = True
        return self

    def __exit__(self, type1, value, traceback):
        if self.connected:
            self.ssh.close()
            self.connected = False

    def __del__(self):
        if self.connected:
            self.ssh.close()
            self.connected = False

    def cast(self, cmd):
        print("cast {0}: {1}".format(self.srv, cmd))
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        data = stdout.read().decode()
        err = stderr.read().decode()
        if err:
            self.err = err
            print("cast error: {}".format(err))
        #print("data: {0}".format(data))
        return data

    def rac(self, *args):
        cmd = "{0} {1}".format(self.rac_pach, " ".join(args))
        data = self.cast(cmd)
        if self.err and not self.init_ras:
            self.init_ras = True
            self.err = ""
            #self.regras()
            return self.cast(cmd)
        return data

    def ibcmd(self, *args):
        cmd = "{0} {1}".format(self.ibcmd_pach, " ".join(args))
        if self.testmode:
            print("TEST: {0}".format(cmd))
        else:
            return self.cast(cmd)

    @staticmethod
    def takekeys(s0):
        d = {}
        for s in s0.split("\n"):
            if s:
                try:
                    k, v = [x.strip() for x in s.split(":")]
                    if not (k in d.keys()):
                        d[k] = []
                    d[k].append(v)
                except ValueError:
                    pass
        kk = []
        if not d:
            return kk
        ml = max([len(d[k]) for k in d.keys()])
        if ml == 0:
            return kk
        for i in range(ml):
            kk.append({})
            for k in d.keys():
                if i < len(d[k]):
                    val = d[k][i]
                else:
                    val = None
                kk[i][k] = val
        return kk

    def init_clusters(self):
        self.clusters_list = []
        for curr_cluster in self.takekeys(self.rac("cluster list | grep cluster")):
            self.clusters_list.append(curr_cluster["cluster"])

    def init_bases(self):
        if not self.clusters_list:
            self.init_clusters()
        self.bases_dict = {}
        for cluster in self.clusters_list:
            cmd = "infobase --cluster={0} summary list".format(cluster)
            for cur_base in self.takekeys(self.rac(cmd)):
                cur_base["cluster"] = cluster
                self.bases_dict[cur_base["name"]] = cur_base




class SessionManager(object):
    """find and destroy user session"""

    def __init__(self, connection):
        super(SessionManager, self).__init__()
        self.conn = connection
        self.testmode = self.conn.testmode
        if not self.conn.bases_dict:
            self.conn.init_bases()

    def current_sessions(self, base):
        cmd = "session --cluster={cluster} list --infobase={infobase}"
        cmd = cmd.format(**self.conn.bases_dict[base])
        return self.conn.takekeys(self.conn.rac(cmd))

    def terminate_session(self, cluster, session):
        cmd = "session --cluster={0} terminate --session={1}"
        cmd = cmd.format(cluster, session)
        if self.testmode:
            print("TEST: {0}".format(cmd))
        else:
            self.conn.rac(cmd)

    def terminate_all(self, base):
        cluster = self.conn.bases_dict[base]["cluster"]
        for curr_sess in self.current_sessions(base):
            self.terminate_session(cluster, curr_sess["session"])

    def terminate_sessions(self, base, userlist):
        cluster = self.conn.bases_dict[base]["cluster"]
        for curr_sess in self.current_sessions(base):
            if curr_sess["user-name"] in userlist:
                self.terminate_session(cluster, curr_sess["session"])


class BaseLock(object):
    """block base to make safe backup"""

    def __init__(self, conn, base, usr, pwd):
        super(BaseLock, self).__init__()
        self.conn = conn
        self.base = base
        self.locked = False
        self.testmode = self.conn.testmode
        self.usr = usr
        self.pwd = pwd

    def __enter__(self):
        cmd = "infobase --cluster={cluster} update --infobase={infobase}"
        cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
        cmd = cmd + " --sessions-deny=on --scheduled-jobs-deny=on"
        cmd = cmd + '--denied-message="backup in progress"'
        cmd = cmd.format(**self.conn.bases_dict[self.base])
        if self.testmode:
            print("TEST: {0}".format(cmd))
        else:
            self.conn.rac(cmd)

        self.locked = True
        return self

    def __exit__(self, type1, value, traceback):
        if self.locked:
            cmd = "infobase --cluster={cluster} update --infobase={infobase}"
            cmd = cmd + " --infobase-user={} --infobase-pwd={}".format(self.usr, self.pwd)
            cmd = cmd + " --sessions-deny=off --scheduled-jobs-deny=off"
            cmd = cmd.format(**self.conn.bases_dict[self.base])
            if self.testmode:
                print("TEST: {0}".format(cmd))
            else:
                self.conn.rac(cmd)


class IbcmdManager(object):
    """docstring for IbcmdManager"""

    def __init__(self, connection, srv, base, usr, pwd):
        super(IbcmdManager, self).__init__()
        self.conn = connection
        self.testmode = self.conn.testmode
        # --dbms=MSSQLServer postgresql
        self.bparams = ["--dbms=postgresql"]
        self.bparams.append("--db-server=" + socket.gethostbyname(srv))
        self.bparams.append("--db-name=" + base)
        self.bparams.append("--db-user=" + usr)
        self.bparams.append("--db-pwd=" + pwd)

    def make_req(self, cmd):
        if self.testmode:
            print("TEST: {0}".format(cmd))
        else:
            return self.conn.ibcmd(cmd)

    def infobase_command(self, command, file_pach):
        """dump : make base backup, block base before
        restore : restore base backup, block base before
        config load : update base config, block base before
        config save : backup base config, block base before
        config import
        config export
        config apply --force
         """
        cmd = " ".join(["infobase", command, *self.bparams, file_pach])
        return self.make_req(cmd)


class LocalConnection(object):
    def __init__(self):
        super(LocalConnection, self).__init__()

    def __enter__(self):
        pass

    def __exit__(self, type1, value, traceback):
        pass

    def cast(self, cmd):
        print("cast {0}: {1}".format("LocalHost", cmd))
        data = os.popen(cmd).read()
        return data

class Connection(object):
    def __init__(self, srv="", **kwargs):
        super(Connection, self).__init__()
        if srv == "localhost":
            self.connection = LocalConnection()
        else:
            self.connection = RemoteConnection(**kwargs)


    def __enter__(self):
       conn = self.connection
       return conn

    def __exit__(self, type1, value, traceback):
        pass