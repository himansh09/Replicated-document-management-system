#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
"""
*** Created using spyder 3.2.8
*** Created on Tue Nov  6 04:31:32 2018
*** Author : Himanshu Saraiya
*** Roll Number: 18111023
"""


from utility_functions import database_drivers
import sqlite3

def signup(username, password, name, contact_details):
    conn = sqlite3.connect('./database/database.db')
    cursor = conn.execute(
                            'select * from credentials where username=\''+username+"\'"
                        )
    credential = (cursor.fetchall())
    conn.close()
    print(cursor)
    if cursor:
        return False
    else:
        database_drivers.add_credential([username, password])
        database_drivers.add_user_details(username,name,contact_details)
        print('Signup successful.\n')
        return True
    
def login(username,password):
    conn = sqlite3.connect('./database/database.db')
    cursor = conn.execute(
                            'select * from credentials where username=\''+username+"\'"
                        )
    credential = (cursor.fetchall())
    conn.close()
    if credential[0][1] == password:
        return True
    else:
        return False

signup('Himansh','password','himanshu','contact_details')    
print(login('him','password'))