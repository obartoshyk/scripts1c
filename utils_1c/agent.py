#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import subprocess
import paramiko
import time

if False:
    p = subprocess.Popen([r'/opt/1cv8/x86_64/8.3.20.1613/./1cv8',
                     r'DESIGNER',
                     r'/F /home/baal/projects/bases1c/sales_repozitory',
                     r'/AgentMode',
                     r'/AgentPort 2021',
                     r'/AgentSSHHostKeyAuto',
                     r'/AgentBaseDir /tmp/DESIGNER_tmp'])

time.sleep(5)

host = '127.0.0.1'
#host = 'vps862.dc-sig.gurtam.net'
user = 'baal'
secret = ''
port = 2021

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
#client.connect(hostname=host, port=port, username=user, password=secret)
client.connect(hostname=host, port=port, username=user, password=secret)
               #, key_filename="/home/baal/.ssh/id_rsa")

transport = client.get_transport()
channel = transport.open_session()
channel.invoke_shell()
print(channel.recv(5000).decode('utf-8'))

channel.send('options set --show-prompt=no\n')
time.sleep(3)
print('Нет коммандной строки: ' + channel.recv(5000).decode('utf-8'))

channel.send('common connect-ib\n')
time.sleep(1)
print('Подключение к базе: ' + channel.recv(5000).decode('utf-8'))





#channel.send('common shutdown\n')
#time.sleep(1)
#print('Завершение работы: ' + channel.recv(5000).decode('utf-8'))

channel.send('config dump-cfg --file testagent.cf\n')
time.sleep(1)
print('dump-cfg  : ' + channel.recv(5000).decode('utf-8'))

channel.send('common disconnect-ib\n')
time.sleep(1)
print('Отключение от базы: ' + channel.recv(5000).decode('utf-8'))

channel.close()
client.close()

print("конец программы")