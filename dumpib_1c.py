#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from sets_1c import argparse_1c,settings_1c, connection_1c

if __name__ == "__main__":
	parser =argparse_1c.ArgumentParser_1C("sbd",description=__doc__) 
	parser.decode_arg()
	conn=connection_1c.Connection(parser.s[0],parser.args["test"])
	sm = connection_1c.SessionManager(conn)
	sm.terminate_all(parser.b[0])

	with connection_1c.BaseLock(conn,parser.b[0]):
		#im = connection_1c.IbcmdManager(conn,parser.s[0],parser.b[0],parser.db_usr,parser.db_pwd)
		#im.infobase_config_save("/root/backup/test.cfg")
		pass