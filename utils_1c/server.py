#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from . import comand_1c
from . import basedata

class Server(comand_1c.CommandMaker):
    """Server of 1C info bases"""

    def __init__(self, *args, **kwargs):
        super(Server, self).__init__()
        comand_1c.CommandMaker.__init__(self, *args, command="rac", **kwargs)
        self.clusters_list = []
        self.bases_dict = {}

    def init_clusters(self):
        answ = self.run("cluster list | grep cluster")
        for curr_cluster in self.takekeys(answ):
            self.clusters_list.append(curr_cluster["cluster"])

    def init_bases(self):
        if not self.clusters_list:
            self.init_clusters()
        for cluster in self.clusters_list:
            answ = self.run("infobase", "--cluster={0} summary list".format(cluster))
            for cur_base in self.takekeys(answ):
                cur_base["cluster"] = cluster
                self.bases_dict[cur_base["name"]] = cur_base

    def get_bases(self):
        if not self.bases_dict:
            self.init_bases()
        return self.bases_dict

    def get_base(self, base):
        return self.get_bases()[base]

    def get_clbase(self, base_name="", **kwargs):
        cur_base = self.get_base(base_name)
        return basedata.ClusterBase(cluster=cur_base["cluster"],
                                    infobase=cur_base["infobase"],
                                    usr=kwargs["usr"], pwd=kwargs['pwd'])

    @staticmethod
    def takekeys(s0):
        d = {}
        for s in s0.split("\n"):
            if s:
                try:
                    k, v = [x.strip() for x in s.split(":")]
                    if not (k in d.keys()):
                        d[k] = []
                    d[k].append(v)
                except ValueError:
                    pass
        kk = []
        if not d:
            return kk
        ml = max([len(d[k]) for k in d.keys()])
        if ml == 0:
            return kk
        for i in range(ml):
            kk.append({})
            for k in d.keys():
                if i < len(d[k]):
                    val = d[k][i]
                else:
                    val = None
                kk[i][k] = val
        return kk
