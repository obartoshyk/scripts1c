#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timezone
import os
import subprocess
import time


def str_cur_time():
    lt = time.localtime(time.time())
    return "{}/{:02}/{:02}:{:02}.{:02}.{:02}".format(lt.tm_year,
                                                     lt.tm_mon,
                                                     lt.tm_mday,
                                                     lt.tm_hour,
                                                     lt.tm_min,
                                                     lt.tm_sec)


class FileStorage(object):
    def __init__(self, storage_path="", srv="", trn="", **kwargs):
        super(FileStorage, self).__init__()
        self.srv = srv
        self.storage_path = storage_path
        self.ssh_key = kwargs["ssh_key"]
        self.dirs_file_name = "/tmp/dirs{}.ini".format(trn)
        self.files_file_name = "/tmp/files{}.ini".format(trn)

    def old_files(self, age=365):
        now = datetime.now(timezone.utc)
        old_files = []
        for pach, dirs, files in self.walk():
            for file in files:
                path_to_file = "{}/{}".format(pach, file)
                cr_date = datetime.fromtimestamp(self.stat(path_to_file).st_mtime, tz=timezone.utc)
                if (now - cr_date).days >= age:
                    old_files.append(path_to_file)
        return old_files

    @staticmethod
    def get_import_stream_counter():
        dirs_file_tmpl = "/tmp/dirs{}.ini"
        trn = 0
        n_name = dirs_file_tmpl.format(str(trn))
        while os.path.exists(n_name):
            trn += 1
            n_name = dirs_file_tmpl.format(str(trn))
        return trn - 1

    @staticmethod
    def get_export_stream_counter(old_files):
        if len(old_files) > 1000:
            return 30
        elif len(old_files) > 100:
            return 5
        else:
            return 1

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
        cmd = 'chmod a+rw "{file_path}"'
        self.cast(cmd.format(file_path=file_path))
        return file_path

    def rm_ssh(self, file_path):
        cmd = 'ssh -i "{ssh_key}" "root@{srv}" rm "{file_path}"'
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

    def sync_export(self, old_files):
        self.clear_cache()
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
        if not os.path.exists(self.dirs_file_name):
            print("missing file: ", self.dirs_file_name)
            return 0
        if not os.path.exists(self.files_file_name):
            print("missing file: ", self.files_file_name)
            return 0
        print("sync started: ", str_cur_time())
        self.create_dirs()
        self.create_files()
        print("sync finished: ", str_cur_time())

    def sync_remove(self):
        if not os.path.exists(self.files_file_name):
            print("missing file: ", self.files_file_name)
            return 0
        self.rm_files()
        self.clear_cache()

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
                    if os.path.exists(n_name):
                        self.rm_ssh(n_name)
