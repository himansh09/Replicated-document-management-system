from flask import Flask, render_template
from flask_socketio import SocketIO ,emit,send
import os
import sys
sys.path.insert(0,os.path.join(os.path.dirname(os.path.realpath(__file__)),'../utility_functions/'))
import database_drivers as DB
import random
import utilities
import json


def pushDB(message):
    # Enter the DB entry for lock
    myClusterId = 1
    myIp = "172.17.0.2"
    dbName = "db1"
    clientIndex = message
    indexFile = "/Source/Repo/db1/.mvc/index.json"
    db = DB.retreiveDbClusterMapping(dbName)
    lock = 1
    if (len(db) == 0):
        #This is a new Database
        print(1)
    else:
        fp = open(indexFile)
        serverIndex = json.load(fp)
        consistent = False
        # print(clientIndex['isReverted'],sys.stdout)
        if (clientIndex['isReverted'] == 'True'):
            if (clientIndex['revertedFrom'] == serverIndex['currentVersion']):
                consistent = True
        elif (clientIndex['latestVersion'] == serverIndex['latestVersion']):
            consistent = True
        clusterId = db[0][1]
        if (consistent is True):
            serverIP = None
            if clusterId == myClusterId:
                serverIP = myIp
            else:
                serverIPList = DB.retreiveServerClusterMapping(clusterId)
                i = random.randint(0, len(serverIPList))
                serverIP = serverIPList[i][2]
            zk_client = C.KazooClient(hosts=serverIP)
            zk_client.start()
            lock = zk_client.Lock(dbName)
            lockAcquired = lock.acquire()
            #Add DB Entry and set lock to 1
            

            emit("pushSignal",serverIP)
            #check lock in DB continuously



            #if lock set to 0
            #send replication message to all servers

            lock.release()






def pullDB(message):
    # Find the serverIP which has DB
    # Hardcoded . Read from ConfigFile

    myClusterId = 1
    myIp = "172.17.0.2"
    dbName = "db1"
    db = DB.retreiveDbClusterMapping(dbName)
    # if DB not found Send Error Message
    if(len(db)==0):
        emit("dbNotFound", "dbNotFound")
    else:
        clusterId = db[0][1]
        if clusterId == myClusterId:
            serverIP = myIp
        else:
            serverIPList = DB.retreiveServerClusterMapping(clusterId)
            i = random.randint(0, len(serverIPList))
            serverIP = serverIPList[i][2]
        emit("pullSignal",str(serverIP))
