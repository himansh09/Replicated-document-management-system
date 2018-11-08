#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 04:28:44 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""


import sqlite3

def executeQuery(query_string):
    """
        This function executes the query passed as 'query_string'. User should make sure query is error free. Use with caution.
    """
    try:
        conn = sqlite3.connect('./database/database.db')
        conn.execute(query_string)
    except Exception as e:
        print("Exception [database_insertion_drivers.py:Database] ::-",str(e))
    conn.commit()
    conn.close()

def add_user_details(username,name,contact_details):
    executeQuery('insert into user_details (username,name,contact_details) values(\''+str(username)+'\',\''+str(name)+'\','+str(contact_details)+');')

def add_credential(username,password):
    executeQuery('insert into credentials (username,password) values(\''+str(username)+'\',\''+str(password)+'\');')
    
def add_db_in_cluster(cluster_id,db_name):
    executeQuery('insert into cluster_db(cluster_id,database) values(\''+str(cluster_id)+',\''+str(db_name)+'\');')
    
def add_node_in_cluster(cluster_id,ip):
    executeQuery('insert into cluster_ip(cluster_id,ip) values(\''+str(cluster_id)+',\''+str(ip)+'\');')
    
def add_user_db(cluster_id,db_name):
    executeQuery('insert into user_db(cluster_id,database) values(\''+str(cluster_id)+',\''+str(db_name)+'\');')
    
def add_lock_status(ip,status,db_name):
    query = 'insert into ip_node_status(ip,status,database) values(\''+(ip)+'\','+str(status)+',\''+str(db_name)+'\');'
    executeQuery(query)
    
def add_db_lock(db_name,lock):
    query = 'insert into db_lock(database,lock) values(\''+(db_name)+'\','+str(lock)+');'
    executeQuery(query)
    
def getLockFromDB(db_name):
    query = 'select lock from db_lock where database =\'' + db_name + '\';'
    try:
        conn = sqlite3.connect('./database/database.db')
        cursor = conn.execute(query)
        value = cursor.fetchall()
        lock_val = value[0][0]
    except Exception as e:
        print("Exception [database_insertion_drivers.py:Database] ::-",str(e))
    conn.commit()
    conn.close()
    return lock_val

def getStatusFromIP(ip,db_name):
    query = 'select status from ip_node_status where ip =\'' + ip + '\' and database = \'' + db_name + '\';'
    try:
        conn = sqlite3.connect('./database/database.db')
        cursor = conn.execute(query)
        value = cursor.fetchall()
        status = value[0][0]
    except Exception as e:
        print("Exception [database_insertion_drivers.py:Database] ::-",str(e))
    conn.commit()
    conn.close()
    return status
    
getStatusFromIP('1.1.1.1','abdb')
    
