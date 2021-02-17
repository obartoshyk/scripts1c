#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" 
reg zabbix agent after update version 1C 
"""
from sets_1c import settings_1c, connection_1c, argparse_1c
from io import BytesIO

parser =argparse_1c.ArgumentParser_1C("sk",description=__doc__)
parser.add_argument('-p','--params' ,
				metavar="param:base",
				help='',
				nargs="*",type=str, required=True)
parser.decode_arg()

conn=connection_1c.Connection(srv=parser.s[0],**parser.args)
conn.init_bases()


st = []
b = "UserParameter={param}, {rac_pach} session --cluster={cluster} list --infobase={infobase} | grep -i user-name | wc -l"
n = "UserParameter={param}, {rac_pach} session --cluster={cluster} list | grep -i user-name | wc -l"
for pb in parser.args["params"]:
	param, base = pb.split(':')
	if base:
		st.append(b.format(param=param,
						rac_pach=sets.rac_pach["deb"],
						**conn.bases_dict[base]))
	else:	
		for cluster in conn.clusters_list:
			st.append(n.format(param=param,
						rac_pach=sets.rac_pach["deb"],
						cluster=cluster))

if conn.testmode:
	print("\n".join(st))
else:
	conf_file ="/etc/zabbix/zabbix_agentd.d/userparameter_mysql.conf"
	ftp = conn.ssh.open_sftp()
	ftp.putfo(BytesIO("\n".join(st).encode()), conf_file)
	ftp.close()
	conn.cast("chmod a+r " + conf_file)
	conn.cast("/etc/init.d/zabbix-agent restart")