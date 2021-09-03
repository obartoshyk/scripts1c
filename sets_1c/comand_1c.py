from sets_1c import settings_1c


class RunnerParams(object):
    def __init__(self, *args):
        self.bparams = [*args]

    def getparams(self):
        return self.bparams


class Runner(RunnerParams):
    """ IbCmd server utils"""

    def __init__(self, *args, cmd_func=lambda x: print(x), cmd_pach="TEST", **kwargs):
        RunnerParams.__init__(self, *args)
        self.cmd_func = cmd_func
        self.cmd_pach = cmd_pach

    def run(self, cmd0, *args):
        cmd = self.create_cmd(self.cmd_pach, cmd0, *self.getparams(), *args)
        self.cmd_func(cmd)

    @staticmethod
    def create_cmd(*args):
        return " ".join([*args])


class CommandMaker(Runner):
    def __init__(self, *args, platform="deb", command="ibcmd", **kwargs):
        sets = settings_1c.Settings()
        cmd_pach = getattr(sets, "{}_pach".format(command))[platform]
        Runner.__init__(self, *args, **kwargs, cmd_pach=cmd_pach)
        print(args)
