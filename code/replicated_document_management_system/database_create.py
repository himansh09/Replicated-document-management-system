#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 00:21:25 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import sqlite3
def create_database():
    try:
        conn = sqlite3.connect('./database/database.db')
        conn.execute('''
                     CREATE TABLE cluster_db
                     (s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                     cluster_id INT NOT NULL,
                     database TEXT NOT NULL,
                     FOREIGN KEY(cluster_id) REFERENCES cluster_ip(cluster_id) ON DELETE CASCADE ON UPDATE CASCADE);
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
                     cluster_id INT NOT NULL,
                     ip TEXT NOT NULL);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE user_db
                     (s_no INTEGER PRIMARY KEY AUTOINCREMENT,
                     cluster_id INT NOT NULL,
                     database TEXT NOT NULL,
                     FOREIGN KEY(cluster_id) REFERENCES cluster_ip(cluster_id) ON DELETE CASCADE ON UPDATE CASCADE);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE user_details
                     (username TEXT PRIMARY KEY,
                     name TEXT NOT NULL,
                     contact_details INT,
                     FOREIGN KEY(username) REFERENCES credentials(username) ON DELETE CASCADE ON UPDATE CASCADE);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE db_lock
                     (database TEXT PRIMARY KEY,
                     lock integer NOT NULL,
                     FOREIGN KEY(database) REFERENCES cluster_db(database) ON DELETE CASCADE ON UPDATE CASCADE);
                     ''')
        print("Table created successfully")
        conn.execute('''
                     CREATE TABLE ip_node_status
                     (ip TEXT PRIMARY KEY,
                     status integer NOT NULL,
                     database TEXT NOT NULL,
                     FOREIGN KEY(database) REFERENCES cluster_db(database) ON DELETE CASCADE ON UPDATE CASCADE,
                     FOREIGN KEY(ip) REFERENCES cluster_ip(ip) ON DELETE CASCADE ON UPDATE CASCADE);
                     ''')
        print("Table created successfully")
    except Exception as e:
        print("Exception [database_create.py:Database] ::-",str(e))
    conn.close()
create_database()
    