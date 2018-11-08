#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 03:57:01 2018
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
    
add_user_details('him','heyy',5467456)