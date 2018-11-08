#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 16:05:20 2018

@author: him
"""

import paramiko
import os

###defining prefixes
remote_prefix = "/Source/Repo"
#client_prefix = '/home/him/Documents/distributed_systems/Project/code'

###files and folder to fetch list
#files_to_fetch = ['try/a.pdf','try/b.pdf','try/him.pdf','highlighted_notes/data/ds_highlighted.zip']
#folder_to_fetch = ['highlighted_notes/data/New/']
#sever_ip = '127.0.0.1'
server_username = 'ssh_user'
server_password = 'password'


def fetch_files(server_ip,files_to_fetch,client_prefix):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip,username=server_username,password=server_password)
    #stdin,stdout,stderr=ssh_client.exec_command('ls')
    #print(stdout.readlines())

    ftp_client=ssh_client.open_sftp()
    for file in files_to_fetch:
        directory_name = os.path.dirname(file)
        file_name = os.path.basename(file)
        full_path = os.path.join(client_prefix,directory_name)
        if not os.path.isdir(full_path):
            os.system('mkdir -p {}'.format(full_path))
        ftp_client.get(os.path.join(remote_prefix,file),os.path.join(full_path,file_name))
    #### fetching
    ftp_client.close()

def fetch_folder(server_ip,folder_to_fetch,client_prefix):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=server_ip,username=server_username,password=server_password)
    for folder in folder_to_fetch:
        stdin,stdout,stderr=ssh_client.exec_command('ls -p {}| grep -v /'.format(os.path.join(remote_prefix,folder)))
        files_to_fetch = stdout.readlines()
        stdin,stdout,stderr=ssh_client.exec_command('ls -p {}| grep /'.format(os.path.join(remote_prefix,folder)))
        subfolder_list  = stdout.readlines()
        ## preparing subfolders for recursive call
        if subfolder_list:
            for it,f in enumerate(subfolder_list):
                formatted_filename = f[:-2]
                formatted_filename = formatted_filename.replace(' ','\\')
                subfolder_list[it] = os.path.join(folder,formatted_filename)

        ftp_client=ssh_client.open_sftp()
        for file in files_to_fetch:
            file_name = os.path.basename(file)
            full_path = os.path.join(client_prefix,folder)
            if not os.path.isdir(full_path):
                os.system('mkdir -p {}'.format(full_path))
            ftp_client.get(os.path.join(remote_prefix,folder,file[:-1]),os.path.join(full_path,file_name[:-1]))
        print(subfolder_list)
        if subfolder_list:
            fetch_folder(subfolder_list)

        #### fetching
    ftp_client.close()


#fetch_folder(folder_to_fetch)
 
