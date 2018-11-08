#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 03:01:31 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import sqlite3

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
    
cluster_db_tuple = ((1,('him_db','fsdfs','tetetert')),(2,('fdsfdsf','ytyryry')))
add_db_in_cluster(cluster_db_tuple)