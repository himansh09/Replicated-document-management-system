#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Fri Nov  9 22:58:47 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import paramiko
import os

#remote_prefix = "/Source/Repo"
remote_prefix = "/home/him/test_put"
server_username = 'him'
server_password = 'himme'

def rexists(sftp, path):
    """os.path.exists for paramiko's SCP object
    """
    try:
        sftp.stat(path)
    except IOError as e:
        if e:
            return False
        raise
    else:
        return True

def push_files(server_ip,files_to_push,client_prefix):
    """
        It pushes 'files_to_push' from 'client_prefix' and stores it in 'remote_prefix'
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip,username=server_username,password=server_password)
    #stdin,stdout,stderr=ssh_client.exec_command('ls')
    #print(stdout.readlines())

    ftp_client=ssh_client.open_sftp()
    for file in files_to_push:
        directory_name = os.path.dirname(file)
        file_name = os.path.basename(file)
        full_path = os.path.join(remote_prefix,directory_name)
        #if not os.path.isdir(full_path):
        stdin,stdout,stderr=ssh_client.exec_command('mkdir -p {}'.format(full_path))
        stdin,stdout,stderr=ssh_client.exec_command('chmod 777 {}'.format(full_path))
        ftp_client.put(os.path.join(client_prefix,file),os.path.join(full_path,file_name))
    #### fetching
    ftp_client.close()


def push_folder(server_ip,folder_to_push,client_prefix):
    """
        It puts entire folder 'folder_to_fetch' and it's subfolders and files from 'server_ip', and stores it in 'client_prefix'
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip,username=server_username,password=server_password)
    for folder in folder_to_push:
        stdout=os.popen('ls -p {}| grep -v /'.format(os.path.join(client_prefix,folder))).read()
        files_to_fetch = list(filter(bool, stdout.split('\n')))
        stdout=os.popen('ls -p {}| grep /'.format(os.path.join(client_prefix,folder))).read()
        subfolder_list  = list(filter(bool, stdout.split('\n')))
        ## preparing subfolders for recursive call
        if subfolder_list:
            for it,f in enumerate(subfolder_list):
                formatted_filename = f.replace(' ','\\')
                subfolder_list[it] = os.path.join(folder,formatted_filename)

        ftp_client=ssh_client.open_sftp()
        for file in files_to_fetch:
            file_name = os.path.basename(file)
            full_path = os.path.join(remote_prefix,folder)
            if not rexists(ftp_client,full_path):
                stdin,stdout,stderr=ssh_client.exec_command('mkdir -p {}'.format(full_path))
                stdin,stdout,stderr=ssh_client.exec_command('chmod 777 {}'.format(full_path))
            print(os.path.join(client_prefix,folder,file),'\n')
            ftp_client.put(os.path.join(client_prefix,folder,file),os.path.join(full_path,file_name))
        #print(subfolder_list)
        if subfolder_list:
            push_folder(server_ip,subfolder_list,client_prefix)
        #### fetching
    ftp_client.close()

push_files('localhost',['a.pdf'],'/home/him/')