#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" reg 'ras' after update version 1C"""
from sets_1c import settings_1c, connection_1c, argparse_1c

parser =argparse_1c.ArgumentParser_1C("Sk",description=__doc__)
parser.decode_arg()
#/opt/1cv8/x86_64/8.3.18.1289/ras --daemon cluster
sets = settings_1c.Settings()

for srv in parser.s:
	with connection_1c.Connection(srv=srv,**parser.args) as conn:
		conn.regras()
