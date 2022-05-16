#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""uses bases_tmpl_list.py /home/baal/projects/scripts /home/baal/.ssh/id_rsa /home/baal/projects/scripts1c"""
import sys
import os


def create_bases_list(scripts, ssh_key):
    bases_tmpl = "/".join([scripts, "bases.tmpl"])
    bases_list = "/".join([scripts, "bases.list"])
    if not os.path.exists(bases_list):
        os.mkdir(bases_list)
    for root, dirs, files in os.walk(bases_list):
        for file_path in files:
            os.remove("{}/{}".format(root, file_path))
    for root, dirs, files in os.walk(bases_tmpl):
        for source_file_path in files:
            with open("{}/{}".format(root, source_file_path), "r") as source_file:
                with open("{}/{}".format(bases_list, source_file_path), "w") as target_file:
                    for line in source_file:
                        if line:
                            if line.find("&SSH&"):
                                target_file.write(line.replace("&SSH&", ssh_key))
                            else:
                                target_file.write(line)


def create_Paches(scripts, scripts1c):
    paches_tmpl = "/".join([scripts, "sh/.cfg/Paches.tmpl"])
    paches_cfg = "/".join([scripts, "sh/.cfg/Paches.cfg"])
    with open(paches_tmpl, "r") as source_file:
        with open(paches_cfg, "w") as target_file:
            for line in source_file:
                if line:
                    if line.find("&scripts&"):
                        target_file.write(line.replace("&scripts&", scripts))
                    elif line.find("&scripts1c&"):
                        target_file.write(line.replace("&scripts1c&", scripts1c))
                    else:
                        target_file.write(line)


create_bases_list(sys.argv[1], sys.argv[2])
create_Paches(sys.argv[1], sys.argv[3])
