#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""uses bases_tmpl_list.py /home/baal/projects/scripts/bases.tmpl /home/baal/.ssh/id_rsa"""
import sys
import os
ssh_key = sys.argv[2]
bases_tmpl = sys.argv[1]
bases_list = "{}/bases.list".format("/".join(bases_tmpl.split("/")[:-1]))
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
