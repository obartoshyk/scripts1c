#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" 
terminate 1C current client sessions, it is working only on deb servers for now 
"""
from utils_1c import connection_1c, argparse_1c, server, sessionmanager


def terminate(sm, base, c):
	if c:
		sm.terminate_sessions(base, c)
	else:
		sm.terminate_all(base)


parser = argparse_1c.ArgumentParser_1C("SBCkf", description=__doc__)
parser.decode_arg()
if not(parser.args["base"]) and not(parser.args["client"]):
	raise "I can`t ruin everything again!"


for srv in parser.args["server"]:
	with connection_1c.Connection(srv=srv, **parser.args) as conn:
		server1c = server.Server(cmd_func=conn.cast, platform=parser.args["platform"])
		sm = sessionmanager.SessionManager(server1c)
		server1c.init_clusters()
		server1c.init_bases()
		for base_name in parser.args["base"] if parser.args["base"] else server1c.get_bases():
			sm.terminate_all(base_name)
			#terminate(sm, base_name, parser.args["client"])
