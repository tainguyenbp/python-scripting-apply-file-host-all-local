import csv
import os
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
            scp.close()
            print('Done !!! copy file hosts to client')

    except Exception as e:
            print('Establish connection SCP to client failed')
            print(e)

def ssh_connect_scp_file(host, port, user, password):
    try:
        ssh = paramiko.SSHClient()
        print('Start connect ssh to client')
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)
        scp_file_to_client(ssh)
        ssh.close()

    except Exception as e:
        print('Establish connection SSH to client failed')
        print(e)


if __name__=='__main__':

    if os.path.isfile('hosts'):
            if os.path.isfile('server.csv'):

                with open('server.csv','r') as open_file_csv:

                    read_file_csv = csv.reader(open_file_csv, delimiter=',')

                    next(open_file_csv) # skip header

                    for row in read_file_csv:
                        print('===================================================================================')
                        
                        host = row[0]
                        print('Ip Host:', host)
                        port = row[3]
                        print('Port Connect:', port)
                        user = row[1]
                        print('Username:',user)
                        password = row[2]
                        print('Password:',password)

                        ssh_connect_scp_file(host, port, user, password)

            else:
                print ('File server.csv not exists')
    else:
        print('File hosts not exists')
