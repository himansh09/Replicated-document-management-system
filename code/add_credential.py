#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 03:01:31 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""

import sqlite3

def add_credential(credential):
    username1,password1 = credential
    conn = sqlite3.connect('./database/database.db')
    conn.execute(
                'insert into credentials (username,password) values(\''+str(username1)+'\',\''+str(password1)+'\')'
                )
    print('Value inserted',username1,' ',password1)
    conn.commit()
    conn.close()
    
add_credential(['him','password'])