import csv
import os
import paramiko
from scp import SCPClient

def remove_row_empty_file_csv_use_bash():

    try:
        cmd_get_pwd = os.getcwd()
        cmd_remove_all_row_empty = ('sed -i /^$/d ' + cmd_get_pwd + '/server.csv')
        os.system(cmd_remove_all_row_empty)

    except Exception as e:
        print('Command does not work !!! Please edit code')
        print(e)

def scp_file_to_client(ssh):
    try:
        with SCPClient(ssh.get_transport()) as scp:
            print('Copy file hosts to client')
            scp.put('hosts', '/etc/hosts')
            scp.close()
            print('Done !!! copy file hosts to client')

    except Exception as e:
            print('Establish connection SCP to client failed !!!')
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
        print('Establish connection SSH to client failed !!!')
        print(e)


if __name__=='__main__':

    if os.path.isfile('hosts'):
            if os.path.isfile('server.csv'):

                remove_row_empty_file_csv_use_bash()

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
                open_file_csv.close()
            else:
                print ('File server.csv not exists !!! ')
    else:
        print('File hosts not exists !!!')
