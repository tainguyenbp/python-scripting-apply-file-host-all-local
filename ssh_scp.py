#!/usr/bin/env python
#!/home/tainguyen/code/venv python

import csv
import os
from os import path
import sys
from itertools import combinations
import paramiko
from scp import SCPClient


def ssh_command(ssh):
    command = input("Command:")
    ssh.invoke_shell()
    stdin, stdout, stderr = ssh.exec_command(command)
    print(stdout.read())

def scp_file_to_client(ssh):
    try:
        with SCPClient(ssh.get_transport()) as scp:
            print('Copy file hosts to client')
            scp.put('server.csv', '/home/server.csv')
            print('Done !!! copy file hosts to client')

    except Exception as e:
            print('Establish connection scp failed')
            print(e)

def ssh_connect_scp_file(host, port, user, password):
    try:
        ssh = paramiko.SSHClient()
        print('Start connect ssh to client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)
        scp_file_to_client(ssh)

    except Exception as e:
        print('Establish connection ssh failed')
        print(e)


if __name__=='__main__':

    if os.path.isfile('hosts'):
            if os.path.isfile('server.csv'):

                with open('server.csv','r') as csvfile:

                    readCSV = csv.reader(csvfile, delimiter=',')
                    for row in readCSV:
                        print('===================================================================================')
                        
                        host = row[0]
                        print('Ip Host: ', host)
                        port = row[3]
                        print('Port Connect: ', port)
                        user = row[1]
                        print('Username: ',user)
                        password = row[2]
                        print('Password: ',password)

                        ssh_connect_scp_file(host, port, user, password)
            else:
                print ('File server.csv not exists')
    else:
        print('File hosts not exists')
