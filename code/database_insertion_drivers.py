#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 04:28:44 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""


import sqlite3

def add_user_details(username,name,contact_details):
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into user_details (username,name,contact_details) values(\''+str(username)+'\',\''+str(name)+'\','+str(contact_details)+')'
                )
    conn.commit()
    conn.close()


def add_credential(credential):
    username1,password1 = credential
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into credentials (username,password) values(\''+str(username1)+'\',\''+str(password1)+'\')'
                )
    print('Value inserted',username1,' ',password1)
    conn.commit()
    conn.close()
    
def add_db_in_cluster(cluster_db_tuple):
    conn = sqlite3.connect('./database/database.db')
    for cluster_db_pair in cluster_db_tuple:
        cluster_id, nodes = cluster_db_pair
        for db in nodes:
            conn.execute(
                        'insert into cluster_db(cluster_id,database) values('+str(cluster_id)+',\''+str(db)+'\')'
                        )
            print('Value inserted',cluster_id,' ',db)
    conn.commit()
    conn.close()
    
def add_node_in_cluster(cluster_ip_tuple):
    conn = sqlite3.connect('./database/database.db')
    for cluster_ip_pair in cluster_ip_tuple:
        cluster_id, nodes = cluster_ip_pair
        for ip in nodes:
            conn.execute(
                        'insert into cluster_ip(cluster_id,ip) values('+str(cluster_id)+',\''+str(ip)+'\')'
                        )
            print('Value inserted',cluster_id,' ',ip)
    conn.commit()
    conn.close()
    
def add_user_db(user_db_tuple):
    conn = sqlite3.connect('./database/database.db')
    for user_db_pair in user_db_tuple:
        cluster_id, dbs = user_db_pair
        for db in dbs:
            conn.execute(
                        'insert into user_db(cluster_id,database) values('+str(cluster_id)+',\''+str(db)+'\')'
                        )
            print('Value inserted',cluster_id,' ',db)
    conn.commit()
    conn.close()
    