# -*- coding: UTF-8 -*-

class Repository(object):
    """Server of 1C info bases"""

    def __init__(self, pach0):
        super(Repository, self).__init__()
        self.pach = "{}/conf".format(pach0)
        self.gitdir = "{}/.git".format(pach0)

    def fcmd_list(self, cmd_list):
        return [x % {"pach": self.pach} for x in cmd_list]

    def get_pull_cmd(self, branch):
        cmd_list = ["cd {}".format(self.pach),
                    'git -C "%(pach)s" pull {0}'.format(branch)]
        return self.fcmd_list(cmd_list)

    def get_commit_cmd(self, text):
        cmd_list = ["cd {}".format(self.pach),
                    'git -C "%(pach)s" add .',
                    'git -C "%(pach)s" commit -m "{0}"'.format(text)]
        return self.fcmd_list(cmd_list)

    def get_push_cmd(self):
        cmd_list = ["cd %(pach)s",
                    'git -C "%(pach)s" push']
        return self.fcmd_list(cmd_list)

    def get_start_reload_cmd(self):
        cmd_list = ['[ -d "/tmp/tmpxml" ] && rm -r /tmp/tmpxml',
                    'rm "%(pach)s/ConfigDumpInfo.xml"',
                    'mkdir /tmp/tmpxml']
        for cmd in self.get_pull_cmd("origin master"):
            cmd_list.append(cmd)
        return self.fcmd_list(cmd_list)

    def get_end_reload_cmd(self):
        cmd_list = ['cp /tmp/tmpxml/ConfigDumpInfo.xml "%(pach)s/ConfigDumpInfo.xml"',
                    'rm -r /tmp/tmpxml']
        return self.fcmd_list(cmd_list)
