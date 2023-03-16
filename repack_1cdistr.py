#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""repack client distr after update version 1C and sent to srv"""
import os
import shutil
from utils_1c import settings_1c, argparse_1c

def send_to_srv(sets,update_sets,srv_list, ssh_key):
	#scp -r $pach0/$t_name.zip  root@SRV:/root/install/$t_name.zip
	dest = "{0}/{1}.zip".format(sets.update_cat,update_sets["upd_name"])
	cmd_list = []
	for srv in srv_list: 
		cmd = "scp -i {0} -r {1} root@{2}:/var/www/html/distr1c/new/{3}.zip".format(ssh_key,dest,srv,update_sets["upd_name"])
		cmd_list.append(cmd)
	if sets.test_mode:
		for cmd in cmd_list:
			print(cmd)
	else:	
		for cmd in cmd_list:
			os.system(cmd)

def repack_win(sets,update_sets):
	"""~/8.3.18.1289/setuptc64_8_3_18_1289.rar"""
	sourse = "{0}/{1}{2}.rar".format(sets.update_cat,update_sets['source_name'],sets.version_1C_)
	tcat = "{0}/{1}".format(sets.update_cat,update_sets['upd_name'])
	dest = "{0}.zip".format(tcat)
	if sets.test_mode:
		print("win: {0} =~> {1} =~> {2}".format(sourse,tcat,dest))
	else:	
		os.mkdir(tcat)
		os.system("unrar x {0} {1}/".format(sourse,tcat))
		os.system("zip -j -r {0} {1}/*".format(dest,tcat))
		shutil.rmtree(tcat, ignore_errors=True)
		os.system("chmod a+r {0}".format(dest))

def repack_osx(sets,update_sets):
	"""~/8.3.18.1289/thin.osx_8_3_18_1289.dmg"""
	sourse = "{0}/{1}{2}.dmg".format(
						sets.update_cat,
						update_sets['source_name'],
						sets.version_1C_)
	dest = "{0}/{1}.dmg".format(sets.update_cat,update_sets["upd_name"])
	if sets.test_mode:
		print("osx: {0} =~> {1}".format(sourse,dest))
	else:	
		os.system("cp {0} {1}".format(sourse,dest))
		os.system("chmod a+r {0}".format(dest))

def repack_deb(sets,update_sets):
	#mkdir $pach0/$t_name
	#sudo unrar x $pach0/$b_name$ver1Ck.rar $pach0/$t_name/
	#sudo zip -j -r $pach0/$t_name.zip $pach0/$t_name/*
	#rm -R $pach0/$t_name
	#sudo chmod a+r $pach0/$t_name.zip
	sourse = "{0}/{1}{2}.tar.gz".format(sets.update_cat,update_sets['source_name'],sets.version_1C_)
	tcat = "{0}/{1}".format(sets.update_cat,update_sets['upd_name'])
	dest = "{0}.run".format(tcat)
	if sets.test_mode:
		print("deb: {0} =~> {1} =~> {2}".format(sourse, tcat, dest))
	else:	
		os.mkdir(tcat)
		os.system("tar -C {1} -zxvf {0}".format(sourse, tcat))
		os.system("zip -j -r {0} {1}/*".format(dest, tcat))
		shutil.rmtree(tcat, ignore_errors=True)
		os.system("chmod a+r {0}".format(dest))


if __name__ == "__main__":
	sets = settings_1c.Settings()
	parser =argparse_1c.ArgumentParser_1C("Sk",description=__doc__)
	parser.add_argument('-r','--repack' ,help='Repack archives mode',action='store_true', default=False, required=False)
	parser.add_argument('-p','--update_cat' ,	metavar="~PACH",help='pach to update distr(+ add v.1C)',nargs=1,type=str, required=True)
	parser.decode_arg()
	sets.test_mode = parser.args["test"]

	sets.update_cat=sets.update_distr_cat.replace("%update_distr_cat%",parser.args["update_cat"][0])
	sets.update_cat=sets.update_cat.replace("%version_1C%",sets.version_1C)
	repack = {"win":repack_win,"deb":repack_deb,"osx":repack_osx}
	for upd_name in sets.update_sets:
		if parser.args["repack"]:
			repack[sets.update_sets[upd_name]["method"]](sets,sets.update_sets[upd_name])
		if parser.args["server"]:
			send_to_srv(sets, sets.update_sets[upd_name], parser.args["server"], parser.args["ssh_key"][0])