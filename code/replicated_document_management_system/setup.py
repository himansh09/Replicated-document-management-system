#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Fri Nov  9 20:27:11 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""
import configparser
from utility_functions import database_create
from utility_functions import database_drivers

database_create.create_database('/database/database.db')
conf = configparser.ConfigParser()
conf.read('conf/server.conf')
server_ip = conf['server_conf']['ip']
server_prefix = conf['server_conf']['prefix']
server_cluster = conf['server_conf']['cluster_id']
server_neighbors = conf['server_conf']['neighbors']
print(server_neighbors)
