#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timezone


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
        self.create_pach(pach)
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
