#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" 
terminate 1C current client sessions, it is working only on deb servers for now 
"""
from sets_1c import settings_1c, connection_1c, argparse_1c

def terminate(sm, base, c):
	if c:
		sm.terminate_sessions(base,c)
	else:
		sm.terminate_all(base)

if __name__ == "__main__":
	parser =argparse_1c.ArgumentParser_1C("SBCk",description=__doc__) 
	parser.decode_arg()
	if not(parser.args["base"]) and not(parser.args["client"]):
		raise "I simple can`t ruin everything!"

	for srv in parser.s:
		conn=connection_1c.Connection(srv=srv,**parser.args)
		sm  =connection_1c.SessionManager(conn)
		for base in (parser.b if parser.b else conn.bases_dict.keys()):
			terminate(sm, base, parser.c)

