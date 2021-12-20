# -*- coding: UTF-8 -*-

from . import comand_1c


class DesignerCommand(comand_1c.CommandMaker):

    def __init__(self, *args, **kwargs):
        comand_1c.CommandMaker.__init__(self, *args, command="designer", **kwargs)

#    def run(self, *args):
#        cmd = super(DesignerCommand, self).create_cmd(self.cmd_pach, *self.getparams(), *args)
#        return self.cmd_func(cmd)

    def DumpIB(self, tmpfile=""):
        return self.run("", "/DumpIB", tmpfile)

    def RestoreIB(self, tmpfile):
        pass
        #return self.run("/RestoreIB", tmpfile)

    def DumpCfg(self, tmpfile):
        return self.run("", "/DumpCfg", tmpfile)

    def LoadCfg(self, tmpfile):
        return self.run("", "/LoadCfg", tmpfile)

    def LoadCfgUPD(self, tmpfile):
        return self.run("", "/LoadCfg", tmpfile, "/UpdateDBCfg", "-Dynamic+")

    def UpdateDBCfg(self):
        return self.run("", "/UpdateDBCfg", "-Dynamic+")

    def DumpConfigToFiles(self, tmpfile):
        return self.run("", "/DumpConfigToFiles", tmpfile)

    def LoadConfigFromFiles(self, tmpfile):
        return self.run("", "/LoadConfigFromFiles", tmpfile)

    def LoadConfigFromFilesUPD(self, tmpfile):
        return self.run("", "/LoadConfigFromFiles", tmpfile, "/UpdateDBCfg", "-Dynamic+")

    def RollbackCfg(self):
        return self.run("", "/RollbackCfg")



