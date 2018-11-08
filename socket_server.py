#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Wed Nov  7 14:06:21 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import socket
import pickle
host = 'localhost'     #myip - read from env
port = 23350           #listening port on server

def start_synchronization():
    print('i am here')

def driver_program_socket_listener(server_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((server_ip, port))
        while True:
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(64)
                    try:
                        received_message = pickle.loads(data);
                    except:
                        print('Closing server bacause of pickle')
                        s.close()
                        break;
                    print(received_message)
                    if received_message[0] == "Replicate":
                        start_synchronization()
                        s.sendall(pickle.dumps(["Replication_successful"]))
    except KeyboardInterrupt as kb:
        s.close()
        print('Keyboard interrupt,socket closed successfully')
    except Exception as e:
        print('unable to create socket: ', str(e))
                        
driver_program_socket_listener(host,port)