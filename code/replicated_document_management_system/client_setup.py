#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Fri Nov  9 20:27:11 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""
import configparser
import global_variables

conf = configparser.ConfigParser()
conf.read('conf/client.conf')
client_ip = conf['client_conf']['ip']
client_prefix = conf['client_conf']['prefix']
global_variables.my_ip = client_ip