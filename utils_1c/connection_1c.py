#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import paramiko
import os


class RemoteConnection(object):
    """ Connection to 1C servers uses paramiko"""

    def __init__(self, srv="", **kwargs):
        super(RemoteConnection, self).__init__()
        self.srv = srv
        self.ssh_key = kwargs["ssh_key"]

        self.clusters_list = []
        self.bases_dict = {}
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self) -> object:
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
            raise "cast ERROR: {}".format(err)
        else:
            return data


class LocalConnection(object):
    def __init__(self):
        super(LocalConnection, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self, type1, value, traceback):
        pass

    @staticmethod
    def cast(cmd):
        print("cast {0}: {1}".format("LocalHost", cmd))
        data = os.popen(cmd).read()
        return data


class Connection(object):
    def __init__(self, srv="", **kwargs):
        super(Connection, self).__init__()
        if srv == "localhost":
            self.connection = LocalConnection()
        else:
            self.connection = RemoteConnection(srv=srv, **kwargs)

    def __enter__(self):
        return self.connection.__enter__()

    def __exit__(self, type1, value, traceback):
        self.connection.__exit__(type1, value, traceback)
