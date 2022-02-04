# -*- coding: UTF-8 -*-

class Repository(object):
    """Server of 1C info bases"""

    def __init__(self, pach):
        super(Repository, self).__init__()
        self.pach = pach

    def get_pull_cmd(self, branch):
        cmd_list = ["cd {}".format(self.pach),
                    "git pull {}".format(branch)]
        return cmd_list

    def get_commit_cmd(self, text):
        cmd_list = ["cd {}".format(self.pach),
                    "git add .",
                    'git commit -m "{}"'.format(text)]
        return cmd_list

    def get_push_cmd(self):
        cmd_list = ["cd {}".format(self.pach),
                    "git push"]
        return cmd_list

    def get_start_reload_cmd(self):
        cmd_list = ['[ -d "/tmp/tmpxml" ] && rm -r /tmp/tmpxml',
                    'rm {}/ConfigDumpInfo.xml'.format(self.pach),
                    'mkdir /tmp/tmpxml']
        for cmd in self.get_pull_cmd():
            cmd_list.append(cmd)
        return cmd_list

    def get_end_reload_cmd(self):
        cmd_list = ['cp /tmp/tmpxml/{1} {0}/{1}'.format(self.pach, "ConfigDumpInfo.xml"),
                    'rm -r /tmp/tmpxml']
        return cmd_list
