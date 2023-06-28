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
        self.log = '{}/import/do_not_put_files_here.txt'.format(self.plugin)
        self.exp = []
        self.commits = []
        self.imp = []

    def initialise_export(self):
        self.exp = [(self.plugin, fp) for fp in self.filter_extension_list(self.plugin_export, [".epf", ".erf"])]

    def initialise_import(self):
        self.commits, plugins = self.new_git_data()
        self.imp = self.import_list(plugins)

    def filter_extension_list(self, cat, ext_list):
        epf_ert_list = []
        for pach, dirs, files in self.conn.walk(cat):
            for file in files:
                path_to_file = "{}/{}".format(pach, file)
                file_name, file_extension = os.path.splitext(path_to_file)
                if file_extension in ext_list:
                    epf_ert_list.append(path_to_file)
        return epf_ert_list

    def import_list(self, plugins):
        il = []
        for file in plugins:
            xml = "{}/{}.xml".format(self.plugin, file)
            ext = self.find_import_filename_ext(xml)
            if ext:
                il.append((xml, "{}/import/{}{}".format(self.plugin, file, ext)))
        return il

    def find_import_filename_ext(self, xml_file):
        dt = self.conn.cast("cat {}".format(xml_file))
        if dt.find("ExternalDataProcessorObject") != -1:
            return ".epf"
        if dt.find("ExternalReportObject") != -1:
            return ".erf"
        return ""

    def new_git_data(self):
        log_info = self.get_log_info()
        git_commit_log = self.get_git_commit_log()
        commits = []
        plugins = []
        for commit in git_commit_log.keys():
            if commit not in log_info:
                commits.append(commit)
                for plugin in git_commit_log[commit]:
                    if plugin not in plugins:
                        plugins.append(plugin)
        return commits, plugins

    def get_log_info(self):
        cmd = 'cat {}'.format(self.log)
        return [s for s in self.conn.cast(cmd).split("\n") if s]

    def get_git_commit_log(self):
        cmd = 'git -C "{}" log --oneline --since=1.year --name-only --pretty=format:"N--%h"'.format(self.pach)
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

    def update_log(self):
        s = "\n".join(self.log)
        cmd = 'echo {} > {}'.format(s, self.log)
        self.conn.cast(cmd)

    def clear_export(self):
        for xp, file in self.exp:
            self.conn.rm(file)

    def clear_import(self, sender):
        sender.send_pull_note()
        self.update_log()

