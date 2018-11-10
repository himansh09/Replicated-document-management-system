#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Fri Nov  9 20:27:11 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""
import configparser


conf = configparser.ConfigParser()
conf.read('conf/client.conf')
server_ip = conf['client_conf']['ip']
server_prefix = conf['client_conf']['prefix']
print(server_ip)
print(server_prefix)