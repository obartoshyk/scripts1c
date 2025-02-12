# scripts for managing 1C servers on Linux Debian

**** reg 'ras' after update 1C
./regras.py -s SRV -k %ssh_pach%/.ssh/id_rsa -t 

**** reg zabbix agent after update 1C 
./regzabbix.py -s SRV -k %ssh_pach%/.ssh/id_rsa -t 
   
**** repack client distr after update version 1C and sent to srv
./repack_1cdistr.py -r -p %distr_pach%(+ add v.1C) -k %ssh_pach%/.ssh/id_rsa -s SRV1 SRV2 -t 

**** utils_1c.sessionmanager - terminate current sessions on server
./sessionmanager.py -s SRV1 SRV2 -b BASE1 BASE2 -c CLIENT1 CLIENT2 -k %ssh_pach%/.ssh/id_rsa -t

**** utils_1c.baselock - block/unblock of 1C base 
./baselock.py -s SRV1 -b BASE1 -u USER:PASSWORD -k %ssh_pach%/.ssh/id_rsa -m block/unblock -t

**** utils_1c.config - creation of config backup 
./baselock.py -s SRV1 -b BASE1 -d USER:PASSWORD -k %ssh_pach%/.ssh/id_rsa -m save/load/export/import -t


