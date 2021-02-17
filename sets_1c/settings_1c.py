#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os, time

class Settings(object):
	"""default options to use 1C scripts"""
	def __init__(self):
		super(Settings, self).__init__()
		arg = ""
		wtd = {}
		for action in dir(self):
			if action.find("__cr__") != -1:
				wtd[action] = getattr(self,action) 
		with open("{0}/1csets.ini".format(os.path.dirname(__file__), 'r')) as ini_file:
			for line in ini_file.read().splitlines():
				if line and line[0] != "#":
					argvp = line.find("$$");
					if argvp != -1:
						arg = line[(argvp+2):]
					else:
						parg = "_Settings__cr__{0}".format(arg)
						if parg in wtd:
							wtd[parg](line)
						else:
							self.default_action(arg,line)
		self.init_pach()

	def default_action(self,key,line):
		setattr(self,key,line.strip())

	def default_convfromkey(self,dictname,k,line):
		vals = 	 dict(zip(k, [ x.strip() for x in line.split("|")] ))
		if hasattr(self, dictname):
			dkt = getattr(self, dictname)
		else:
			dkt = {}
		dkt[vals[k[0]]] = vals
		setattr(self,dictname,dkt)

	def __cr__version_1C(self,line):
		self.version_1C = line.strip()
		self.version_1C_="{v[0]}_{v[1]}_{v[2]}_{v[3]}".format(v=self.version_1C.split("."))

	def __cr__servers(self,line):
		self.default_convfromkey("servers",["name","pach" ,"ip","url","tec"],line)

	def __cr__bases(self,line):
		self.default_convfromkey("bases",["name","srv"],line)

	def __cr__update_sets(self,line):
		self.default_convfromkey("update_sets",["upd_name","source_name","method"],line)

	def __new__(self):
		if not hasattr(self, 'instance'):
			self.instance = super(Settings, self).__new__(self)
		return self.instance

	def fdeb(self,strin):
		st1 = strin.replace('%version_1C%',self.version_1C)
		st1 = st1.replace("%deb_pach%",self.deb_pach)
		return st1

	def init_pach(self):
		self.rac_pach =   {"deb": self.fdeb(self.deb_rac_pach)}
		self.ras_pach =   {"deb": self.fdeb(self.deb_ras_pach)}
		self.r1cv8_pach = {"deb": self.fdeb(self.deb_r1cv8_pach)}
		self.ibcmd_pach = {"deb": self.fdeb(self.deb_ibcmd_pach)}

	def srvdict(self,bases):
		srvdict = {}
		for base in bases:
			srv = self.bases[base]["srv"]
		if not srv in srvdict:
			srvdict[srv]=[base]
		else:
			srvdict[srv].append(base)
		return srvdict


class FileManager(object):
	"""manage files to make 1C backups"""
	def __init__(self):
		super(FileManager, self).__init__()
	
	def tmpf(self,path,ext):
		k = 0
		while os.path.exists("{}/tmp{:04}.{}".format(path,k,ext)	): 
			k = k+1
		return 	"{}tmp{:04}.{}".format(path,k,ext)	

	def today_str(self):
		lt = time.localtime(time.time())
		return "{}{:02}{:02}".format(lt.tm_year,lt.tm_mon,lt.tm_mday)
		
	def tmp_pach(self):
		return ""

	def bkp_filename_dt(base):
		sets = settings_1c.Settings()
		#backup_cat = '{0}/{1}'.format(sets.backup_cat,today_str())
		#if not os.path.exists(backup_cat):
		#	os.mkdir(backup_cat)
		#	os.system("chmod a+r {}".format(backup_cat))
		#return self.bkp_cat	
						

