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


def add_credential(username,password):
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into credentials (username,password) values(\''+str(username)+'\',\''+str(password)+'\')'
                )
    print('Value inserted',username,' ',password)
    conn.commit()
    conn.close()
    
def add_db_in_cluster(cluster_id,db):
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into cluster_db(cluster_id,database) values('+str(cluster_id)+',\''+str(db)+'\')'
                )
    print('Value inserted',cluster_id,' ',db)
    conn.commit()
    conn.close()
    
def add_node_in_cluster(cluster_id,ip):
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into cluster_ip(cluster_id,ip) values('+str(cluster_id)+',\''+str(ip)+'\')'
                )
    print('Value inserted',cluster_id,' ',ip)
    conn.commit()
    conn.close()
    
def add_user_db(uname,db):
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into user_db(username,database) values(\''+str(uname)+'\',\''+str(db)+'\')'
                )
    print('Value inserted',uname,' ',db)
    conn.commit()
    conn.close()

def retreiveDbClusterMapping(db):
    conn = sqlite3.connect('./database/database.db')
    cur = conn.cursor()
    cur.execute(
        'select * from cluster_db where database like (\'' + str(db)  + '\')'
    )
    db = cur.fetchall()
    conn.commit()
    conn.close()
    return db

def retreiveServerClusterMapping(clusterId):
    conn = sqlite3.connect('./database/database.db')
    cur = conn.cursor()
    cur.execute(
        'select * from cluster_ip where cluster_id = ' + str(clusterId)
    )
    cluster = cur.fetchall()
    conn.commit()
    conn.close()
    return cluster