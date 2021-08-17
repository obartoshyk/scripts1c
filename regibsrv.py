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
	print(answ)
	if len(answ)>2:
		for k in range(1,len(answ)-1):
			#print("pid:"+answ[k])
			if answ[k] and not conn.testmode: self.cast('kill -9 {0}'.format(answ[k]))


	ftp = conn.ssh.open_sftp()
	for c_file in ftp.listdir(parser.args["pach"][0]):
		if c_file and not conn.testmode:
			print('{0} -c "{1}" --daemon'.format(conn.ibsrv_pach,c_file))	
	if ftp: ftp.close()
	
#test = os.listdir("{dir_name}/{base_name}_local".format(dir_name=dir_name,base_name=base_name))
# 
#s = 'scp -r {dir_name}/{base_name}_local/{f_name} root@vps862.dc-sig.gurtam.net:/home/sandbox/{base_name}/{f_name}' 
#for f_name in test:
#	print(f_name)
#	print(s.format(dir_name=dir_name,base_name=base_name,f_name=f_name))
# 	os.system(s.format(dir_name=dir_name,base_name=base_name,f_name=f_name))