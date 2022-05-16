#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timezone
import os
import subprocess


class FileStorage(object):
    def __init__(self, storage_path="", srv="", **kwargs):
        super(FileStorage, self).__init__()
        self.srv = srv
        self.storage_path = storage_path
        self.ssh_key = kwargs["ssh_key"]

    def old_files(self, age=10):
        now = datetime.now()
        old_files = []
        for pach, dirs, files in self.walk():
            for file in files:
                path_to_file = "{}/{}".format(pach, file)
                cr_date = datetime.fromtimestamp(self.stat(path_to_file).st_mtime, tz=timezone.utc)
                if now.year - cr_date.year > age:
                    old_files.append(path_to_file)
        return old_files

    @staticmethod
    def cast(cmd):
        print("cast {0}: {1}".format("LocalHost", cmd))
        pipe = subprocess.Popen(cmd,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        pipe.communicate()

    @staticmethod
    def stat(dest_dt):
        return os.stat(dest_dt)

    def walk(self):
        return os.walk(self.storage_path)

    def put(self, file_path):
        cmd = 'rsync -az "ssh -i {ssh_key}" "{file_path}" "root@{srv}:{file_path}"'
        self.cast(cmd.format(file_path=file_path, srv=self.srv, ssh_key=self.ssh_key))
        return file_path

    def get(self, file_path):
        cmd = 'rsync -r -e "ssh -i {ssh_key}" root@{srv}:{file_path} {file_path}'
        self.cast(cmd.format(file_path=file_path, srv=self.srv, ssh_key=self.ssh_key))
        return file_path

    def unstorage_path(self, path):
        full_path = ""
        uns_path = "/"
        for dir0 in (x for x in path.split("/") if x):
            full_path = "{}/{}".format(full_path, dir0)
            if full_path == path:
                return uns_path
            if self.storage_path.find(full_path):
                uns_path = "{}{}/".format(uns_path, dir0)

    def get_dirs(self, path):
        dirs = []
        full_path = ""
        split = lambda x: "/" if x else ""
        for dir0 in (x for x in self.unstorage_path(path).split("/") if x):
            full_path = "{}{}{}".format(full_path, split(full_path), dir0)
            dirs.append("{}".format(full_path))
        return dirs

    def get_created_dirs(self, old_files):
        created_dirs = []
        for file_path in old_files:
            for dir in self.get_dirs(file_path):
                if dir not in created_dirs:
                    created_dirs.append(dir)
        return created_dirs

    def create_dirs(self, dirs):
        cmd = 'ssh -i "{ssh_key}" root@{srv} mkdir -p "{dir_}"'
        add_storage = lambda x: "/".join([self.storage_path, x])
        for dir_ in dirs:
            self.cast(cmd.format(dir_=add_storage(dir_),
                                 srv=self.srv,
                                 ssh_key=self.ssh_key))

    def create_files(self, old_files):
        for file_path in old_files:
            self.put(file_path)

    def let_sync(self, age=10):
        old_files = self.old_files(age=age)
        self.create_dirs(self.get_created_dirs(old_files))
        #self.create_files(old_files) - временно отключим
