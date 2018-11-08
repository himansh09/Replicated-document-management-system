#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 03:29:52 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""


import sqlite3
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
            

## example data
user_db_tuple = ((1,('1.1.1.1','1.1.1.2','1.1.1.3')),(2,('1.1.1.4','1.1.1.5')))
add_user_db(user_db_tuple)