#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 00:45:54 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import sqlite3
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
            

## example data
cluster_ip_tuple = ((1,('1.1.1.1','1.1.1.2','1.1.1.3')),(2,('1.1.1.4','1.1.1.5')))
add_node_in_cluster(cluster_ip_tuple)

