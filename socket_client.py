#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Wed Nov  7 17:43:38 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""


import socket
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 23350       # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(['Replicate']))
    s.setblocking(True)
    data = s.recv(64)
    print(pickle.loads(data))
