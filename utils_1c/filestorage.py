#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timezone
import os
import shutil


class FsConnection(object):
    def __init__(self):
        super(FsConnection, self).__init__()

    def move_file(self, tmp_dt, dest_dt):
        self.copy_file(tmp_dt, dest_dt)
        os.remove(tmp_dt)

    @staticmethod
    def copy_file(tmp_dt, dest_dt):
        shutil.copyfile(tmp_dt, dest_dt)

    @staticmethod
    def mkdir(cat):
        os.mkdir(cat)
        os.popen("chmod a+rwx {}".format(cat))
        return cat

    def put(self, pach, srv):
        self.cast("rsync -r --mkpath {pach} root@{srv}:{pach}".format(pach=pach, srv=srv))
        os.remove(pach)
        return pach

    def get(self, pach, srv):
        self.cast("rsync -r root@{srv}:{pach} {pach}".format(pach=pach, srv=srv))
        return pach


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

    @staticmethod
    def rm(dest_dt):
        os.remove(dest_dt)
        return dest_dt


class FileStorage(object):
    def __init__(self, conn, pach):
        super(FileStorage, self).__init__()
        self.conn = conn
        self.pach = pach

    def old_files(self, age=10):
        now = datetime.now()
        old_files = []
        for pach, dirs, files in self.conn.walk(self.pach):
            for file in files:
                path_to_file = "{}/{}".format(pach, file)
                cr_date = datetime.fromtimestamp(self.conn.stat(path_to_file).st_mtime, tz=timezone.utc)
                if now.year - cr_date.year > age:
                    old_files.append(path_to_file)
        return (corr for corr in old_files)

    def put(self, pach):
        self.conn.put(pach, pach)

    def create_pach(self, pach):
        dirp = ""
        for dir0 in (x for x in pach.split("/") if x):
            dirp = "{}/{}".format(dirp, dir0)
            if dirp != pach and not self.exists(dirp):
                self.conn.mkdir(dirp)

    def get(self, pach):
        self.conn.get(pach, pach)

    def exists_sync(self, pach, rst):
        if not self.exists(pach):
            rst.conn.get(pach, pach)

    def exists(self, pach):
        return self.conn.exists(pach)

    def rm(self, pach):
        return self.conn.rm(pach)
