#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" 
reg ibsrv daemon from conf on remote server
"""
from sets_1c import settings_1c, connection_1c, argparse_1c
parser =argparse_1c.ArgumentParser_1C("sk",description=__doc__)
parser.add_argument('-p','--pach' ,
				metavar="pach",
				help='ibsrv conf pach',
				nargs="*",type=str, required=True)
parser.decode_arg()

with connection_1c.Connection(srv=parser.s[0],**parser.args) as conn:
	answ=conn.cast('ps -C ibsrv --format "pid"').split("\n")
	if len(answ)>2:
		for k in range(1,len(answ)-1):
			cmd = 'kill -9 {0}'.format(answ[k])
			conn.cast(cmd) if answ[k] and not conn.testmode else print(cmd)

	ftp = conn.ssh.open_sftp()
	for c_file in ftp.listdir("{pach}/conf".format(pach=parser.args["pach"][0])):
		basename = c_file.replace(".yaml","")
		cmd = '{ibsrv_pach} -c "{pach}/conf/{basename}.yaml" --data "{pach}/{basename}_wdr" --daemon'.format(
			ibsrv_pach=conn.ibsrv_pach
			,pach=parser.args["pach"][0]
			,basename=basename)
		conn.cast(cmd) if not conn.testmode else print(cmd)
	if ftp: ftp.close() 