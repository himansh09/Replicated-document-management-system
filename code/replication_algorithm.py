#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Fri Nov  9 16:31:59 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import fetch_files
import os

db_name_requested = "abdb"
server_ip_from_request = ""
remote_prefix = "/Source/Repo/"
client_prefix = remote_prefix
fetch_files.fetch_folder(server_ip_from_request,os.path.join(remote_prefix,db_name_requested,client_prefix))

