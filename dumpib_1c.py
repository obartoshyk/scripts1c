#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from sets_1c import argparse_1c,settings_1c, connection_1c

parser =argparse_1c.ArgumentParser_1C("sbudk",description=__doc__) 
parser.decode_arg()

with connection_1c.Connection(srv=parser.s[0],**parser.args) as conn:
	sm = connection_1c.SessionManager(conn)
	sm.terminate_all(parser.b[0])
	
	fm = settings_1c.FileManager()
	tmp_dt = fm.tmp_bkp_filename_dt(parser.b[0])
	tmp_log = fm.tmp_bkp_filename_log(parser.b[0])

	with connection_1c.BaseLock(conn,parser.b[0],parser.usr,parser.pwd) as bl:
		im = connection_1c.IbcmdManager(conn,parser.s[0],parser.b[0],parser.db_usr,parser.db_pwd)
		print(im.infobase_command("dump",tmp_dt))