#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from sets_1c import argparse_1c,settings_1c, connection_1c

parser =argparse_1c.ArgumentParser_1C("sBudk",description=__doc__) 
parser.add_argument('-p','--pach' ,
				metavar="PACH",
				help='backup cat pach',
				nargs="*",type=str, required=True)
parser.decode_arg()

fm = settings_1c.FileManager()
fm.init_bkp_pach(parser.args["pach"][0])
srv=parser.s[0]
print("***starting backup srv:",srv)	
with connection_1c.Connection(srv=srv,**parser.args) as conn:

	sm = connection_1c.SessionManager(conn)
	
	for b in parser.b:

		tmp_dt = fm.tmp_bkp_filename(b,"dt")
		dest_dt = fm.dest_bkp_filename(b,"dt")

		print("***starting dump:",b)	
		
		sm.terminate_all(b)

		with connection_1c.BaseLock(conn,b,parser.usr,parser.pwd) as bl:
			im = connection_1c.IbcmdManager(conn,srv,b,parser.db_usr,parser.db_pwd)
			print(im.infobase_command("dump",tmp_dt))

		conn.cast("chmod a+r " + tmp_dt)
		ftp = conn.ssh.open_sftp()
		ftp.get(tmp_dt,dest_dt)
		ftp.remove(tmp_dt)
		if ftp: ftp.close()

		print("***finished dump:",b)

print("***finished backup srv:",srv)		