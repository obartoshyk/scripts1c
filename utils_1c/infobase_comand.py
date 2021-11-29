#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from . import comand_1c


class InfobaseCommand(comand_1c.CommandMaker):

    def __init__(self, *args, **kwargs):
        tmp_file = "/tmp/ibcmd_cat"
        kwargs["cmd_func"]('[ -d "{0}" ] && rm -r {0}'.format(tmp_file))
        kwargs["cmd_func"]("mkdir {0}".format(tmp_file))
        kwargs["cmd_func"]("chmod a+rw {0}".format(tmp_file))
        comand_1c.CommandMaker.__init__(self, *args,  "--data={0}".format(tmp_file), command="ibcmd", **kwargs)

    def config_save(self, tmpfile=""):
        return self.run("infobase config save", tmpfile)

    def config_load(self, tmpfile):
        return self.run("infobase config load", tmpfile)

    def config_export_sync(self, tmpfile):
        return self.run("infobase config export", "--sync", tmpfile)

    def config_export(self, tmpfile):
        return self.run("infobase config export", tmpfile)

    def config_import(self, tmpfile):
        return self.run("infobase config import", tmpfile)

    def config_apply(self):
        return self.run("infobase config apply", "--force")

    def dump(self, tmpfile):
        return self.run("infobase dump", tmpfile)

    def restore(self, tmpfile):
        return self.run("infobase restore", tmpfile)

