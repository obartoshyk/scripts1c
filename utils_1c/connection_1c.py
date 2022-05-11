#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import paramiko
import socket
import shutil
import types
from stat import S_ISDIR, S_ISREG


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
        self.sftp = None
        self.sftp_open = False

    def __enter__(self) -> object:
        self.ssh.connect(hostname=self.srv, username='root', key_filename=self.ssh_key)
        return self

    def __exit__(self, type1, value, traceback):
        if self.sftp_open:
            self.sftp.close()
        self.ssh.close()

    def __del__(self):
        if self.sftp_open:
            self.sftp.close()
        self.ssh.close()

    def get_sftp(self):
        if not self.sftp_open:
            self.sftp = self.ssh.open_sftp()
            self.sftp_open = True
        return self.sftp

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
        ftp = self.get_sftp()
        try:
            ftp.stat(tmp_dt)
            ftp.get(tmp_dt, dest_dt)
            ftp.remove(tmp_dt)
        except IOError:
            print('file {} not exist'.format(tmp_dt))

    def get(self, tmp_dt, dest_dt):
        if self.exists(tmp_dt):
            self.get_sftp().get(tmp_dt, dest_dt)

    def put(self, tmp_dt, dest_dt):
        if self.exists(tmp_dt):
            self.get_sftp().put(tmp_dt, dest_dt)

    def walk(self, curr_dir):
        list_of_f = []
        ftp = self.get_sftp()
        self.listdir_r(ftp, curr_dir, list_of_f)
        return (corr for corr in list_of_f)

    def listdir_r(self, ftp, curr_dir, list_of_f):
        dirs_to_explore = []
        files = []
        for entry in ftp.listdir_attr(curr_dir):
            current_file_or_dir = curr_dir + "/" + entry.filename
            if S_ISDIR(entry.st_mode):
                dirs_to_explore.append(current_file_or_dir)
            elif S_ISREG(entry.st_mode):
                files.append(entry.filename)
        list_of_f.append((curr_dir, dirs_to_explore, files))
        for lower_dir in dirs_to_explore:
            self.listdir_r(ftp, lower_dir, list_of_f)

    def stat(self, pach):
        return self.get_sftp().lstat(pach)

    def exists(self, path):
        try:
            self.get_sftp().stat(path)
        except IOError:
            return False
        return True


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
    def get(tmp_dt, dest_dt):
        shutil.copyfile(tmp_dt, dest_dt)

    @staticmethod
    def put(tmp_dt, dest_dt):
        shutil.copyfile(tmp_dt, dest_dt)

    @staticmethod
    def cast(cmd):
        print("cast {0}: {1}".format("LocalHost", cmd))
        return os.popen(cmd).read()

    @staticmethod
    def walk(dest_dt):
        return os.walk(dest_dt)

    @staticmethod
    def stat(dest_dt):
        return os.stat(dest_dt)

    @staticmethod
    def exists(dest_dt):
        return os.path.exists(dest_dt)


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
