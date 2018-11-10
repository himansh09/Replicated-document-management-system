#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 00:21:25 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import sqlite3
def create_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        conn.execute('''
                     CREATE TABLE cluster_db
                     (s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                     cluster_id TEXT NOT NULL,
                     database TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE credentials
                     (username TEXT PRIMARY KEY NOT NULL,
                     password TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE cluster_ip
                     (s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                     cluster_id TEXT NOT NULL,
                     ip TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE user_db
                     (s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                     username TEXT NOT NULL,
                     database TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE user_details
                     (username TEXT PRIMARY KEY,
                     name TEXT NOT NULL,
                     contact_details TEXT);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE db_lock
                     (database TEXT PRIMARY KEY,
                     lock integer NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE ip_node_status
                     (ip TEXT PRIMARY KEY,
                     status integer NOT NULL,
                     database TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                      create table jobs(
                      job_id primary key,
                      database_name TEXT ,
                      server_ip TEXT)       
                     ''')
        print("Table created successfully")
        conn.close()
    except Exception as e:
        print("Exception [database_create.py:Database] ::-",str(e))
        conn.close()