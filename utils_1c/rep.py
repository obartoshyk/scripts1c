# -*- coding: UTF-8 -*-
import os


class Repository(object):
    """Server of 1C info bases"""

    def __init__(self, parser):
        super(Repository, self).__init__()
        self.pach0 = parser.args["repozitory"][0]
        self.pach = "{}/conf".format(self.pach0)
        self.gitdir = "{}/.git".format(self.pach0)
        self.plugin = "{}/plugin".format(self.pach0)
        self.plugin_export = "{}/export".format(self.plugin)

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


class RepositoryPlugins(Repository):

    def __init__(self, parser, conn):
        Repository.__init__(self, parser)
        self.conn = conn

    def get_convert_list(self):
        return [], [(self.plugin, fp) for fp in self.ft_list(self.plugin_export, [".epf", ".erf"])]

    def ft_list(self, pach, ext_list):
        epf_ert_list = []
        for fp in self.conn.walk(pach):
            file_name, file_extension = os.path.splitext(fp)
            for ext in ext_list:
                if file_extension == ext:
                    epf_ert_list.append("{}/{}".format(pach, fp))
        return epf_ert_list

    def get_pl_files_list(self):
         print(self.get_git_log())

    def get_git_log(self):
        cmd = 'git -C "{}" log --oneline --since=1.day --name-only --pretty=format:"N--%h"'.format(self.pach)
        gl = {}
        commit = ""
        for s in [s for s in self.conn.cast(cmd).split("\n") if s]:
            if s.find("N--") != -1:
                commit = s.replace("N--", "")
                gl[commit] = []
            if s.find("plugin/") != -1:
                sb = os.path.splitext(s.replace("plugin/", "").split("/")[0])[0]
                if sb != "import" and sb != "export":
                    gl[commit].append(sb)
        return {k: gl[k] for k in gl if gl[k]}


