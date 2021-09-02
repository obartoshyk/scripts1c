class RunnerParams(object):
   def __init__(self, *args):
       self.bparams = [*args]

   def getparams(self):
       return self.bparams


class Runner(RunnerParams):
    """ IbCmd server utils"""

    def __init__(self, *args, cmd_func=lambda x: print(x), cmd_pach="TEST_PACH"):
        super(Runner, self).__init__()
        RunnerParams.__init__(self, *args)
        self.cmd_func = cmd_func
        self.cmd_pach = cmd_pach

    def run(self, cmd0, *args):
        cmd = self.create_cmd(self.cmd_pach, cmd0, *self.getparams(), *args)
        self.cmd_func(cmd)

    @staticmethod
    def create_cmd(*args):
        return " ".join([*args])
