# scripts1c

scripts:

**** reg 'ras' after update 1C
./regras.py -s SRV -k %ssh_pach%/.ssh/id_rsa -t 

**** reg zabbix agent after update 1C 
./regzabbix.py -s SRV -k %ssh_pach%/.ssh/id_rsa -t 
   
**** repack client distr after update version 1C and sent to srv
./repack_1cdistr.py -r -p %distr_pach%(+ add v.1C) -k %ssh_pach%/.ssh/id_rsa -s SRV1 SRV2 -t 

**** terminate 1C current client sessions
./terminate_1c.py -s SRV1 SRV2 -b BASE1 BASE2 -c CLIENT1 CLIENT2 -k %ssh_pach%/.ssh/id_rsa -t 