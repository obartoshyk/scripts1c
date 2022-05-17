#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timezone
import os
import subprocess
import time

class FileStorage(object):
    def __init__(self, storage_path="", srv="", **kwargs):
        super(FileStorage, self).__init__()
        self.srv = srv
        self.storage_path = storage_path
        self.ssh_key = kwargs["ssh_key"]
        self.dirs_file_name = "/tmp/dirs.ini"
        self.files_file_name = "/tmp/files.ini"

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
        cmd = 'scp -i "{ssh_key}" "{file_path}" "root@{srv}:{file_path}"'
        self.cast(cmd.format(file_path=file_path, srv=self.srv, ssh_key=self.ssh_key))
        return file_path

    def get(self, file_path):
        cmd = 'scp -i "{ssh_key}" root@{srv}:{file_path} {file_path}'
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

    def sync_export(self, age=10):
        self.clear_cache()
        old_files = self.old_files(age=age)
        self.create_dir_file(self.get_created_dirs(old_files))
        self.create_files_file(old_files)
        self.send_ini()

    def clear_cache(self):
        if os.path.exists(self.dirs_file_name):
            os.remove(self.dirs_file_name)
        if os.path.exists(self.files_file_name):
            os.remove(self.files_file_name)

    def create_dir_file(self, dirs):
        add_storage = lambda x: "{}\n".format("/".join([self.storage_path, x]))
        with open(self.dirs_file_name, "w") as target_file:
            target_file.writelines(list(map(add_storage, dirs)))

    def create_files_file(self, old_files):
        add_nl = lambda x: "{}\n".format(x)
        with open(self.files_file_name, "w") as target_file:
            target_file.writelines(list(map(add_nl, old_files)))

    def send_ini(self):
        self.put(self.dirs_file_name)
        self.put(self.files_file_name)
        self.clear_cache()

    def sync_import(self):
        if os.path.exists(self.dirs_file_name):
            print("missing file: ", self.dirs_file_name)
            return 0
        if os.path.exists(self.files_file_name):
            print("missing file: ", self.files_file_name)
            return 0
        print("sync started: ", self.str_cur_time())
        self.create_dirs()
        self.create_files()
        #self.clear_cache()
        print("sync finished: ", self.str_cur_time())

    def create_dirs(self):
        with open(self.dirs_file_name, "r") as target_file:
            for line in target_file:
                n_name = line.rstrip('\n')
                if n_name:
                    if not os.path.exists(n_name):
                        os.mkdir(n_name)

    def create_files(self):
        with open(self.files_file_name, "r") as target_file:
            for line in target_file:
                n_name = line.rstrip('\n')
                if n_name:
                    if not os.path.exists(n_name):
                        self.get(n_name)

    def rm_files(self):
        with open(self.files_file_name, "r") as target_file:
            for line in target_file:
                n_name = line.rstrip('\n')
                if n_name:
                    if not os.path.exists(n_name):
                        self.get(n_name)

    def str_cur_time(self):
        lt = time.localtime(time.time())
        return "{}/{:02}/{:02}:{:02}.{:02}.{:02}".format(lt.tm_year,
                                                         lt.tm_mon,
                                                         lt.tm_mday,
                                                         lt.tm_hour,
                                                         lt.tm_min,
                                                         lt.tm_sec)
