#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import paramiko
import socket
import shutil
import types


def localhost(srv):
    return srv == "localhost" or srv == socket.gethostname()


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
        return self

    def __exit__(self, type1, value, traceback):
        self.ssh.close()

    def __del__(self):
            self.ssh.close()

    def cast(self, cmd):
        print("cast {0}: {1}".format(self.srv, cmd))
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        data = stdout.read().decode()
        err = stderr.read().decode()
        if err:
            print("cast ERROR: {}".format(err))
        else:
            return data

    def move_file(self, tmp_dt, dest_dt):
        ftp = self.ssh.open_sftp()
        try:
            ftp.stat(tmp_dt)
            ftp.get(tmp_dt, dest_dt)
            ftp.remove(tmp_dt)
        except IOError:
            print('file {} not exist'.format(tmp_dt))
        finally:
            if ftp:
                ftp.close()


class LocalConnection(object):
    def __init__(self):
        super(LocalConnection, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self, type1, value, traceback):
        pass

    def move_file(self, tmp_dt, dest_dt):
        self.copy_file(tmp_dt, dest_dt)
        os.remove(tmp_dt)

    @staticmethod
    def copy_file(tmp_dt, dest_dt):
        shutil.copyfile(tmp_dt, dest_dt)

    @staticmethod
    def cast(cmd):
        print("cast {0}: {1}".format("LocalHost", cmd))
        return os.popen(cmd).read()


class Connection(object):
    def __init__(self, srv="", **kwargs):
        super(Connection, self).__init__()
        if localhost(srv):
            self.connection = LocalConnection()
        else:
            self.connection = RemoteConnection(srv=srv, **kwargs)
        self.connection.ps_grep = types.MethodType(self.ps_grep, self.connection)
        self.connection.kill = types.MethodType(self.kill, self.connection)

    def __enter__(self):
        return self.connection.__enter__()

    def __exit__(self, type1, value, traceback):
        self.connection.__exit__(type1, value, traceback)

    @staticmethod
    def ps_grep(conn, grep_list):
        proc_list = []
        if not grep_list:
            return proc_list
        cmd = "ps x"
        for grep_cmd in grep_list:
            cmd = "{} | grep {}".format(cmd, grep_cmd)
        for str_answ in conn.cast(cmd).split("\n"):
            for wrd in str_answ.split(" "):
                if wrd:
                    proc_list.append(wrd)
                    break
        if proc_list:
            proc_list.pop()
        return proc_list

    @staticmethod
    def kill(conn, pid):
        if pid:
            cmd = "kill {}".format(pid)
            return conn.cast(cmd)
        return ""
