import sys

import random

from flask_socketio import SocketIO
from flask import Flask
from flask import request
import utilities
import kazoo.client as C
import database_drivers as DB


app= Flask(__name__)



@app.route("/push",methods = ['POST','GET'])
def checkConsistencyAndPush():

    #Hardcoded . Read from ConfigFile
    myClusterId = 1
    myIp = "172.17.0.2"

    lockAcquired = False
    lock = None
    db_name = ""
    clientIndex = request.values
    dbName = clientIndex['databaseName']
    #Check if  dbRepo already exists in sqlDatabase
    db = DB.retreiveDbClusterMapping("db1")
    if(len(db)!=0):
        create = 1


    #check if Db locally present
    clusterId = db[0][1]
    if clusterId == myClusterId:
        serverIP = myIp
    else:
        serverIPList = DB.retreiveServerClusterMapping(clusterId)
        i = random.randint(0,len(serverIPList))
        serverIP = serverIPList[i][2]


    # Index file should be from right server
    indexFile = "/Source/Repo/db1/.mvc/index.json"


    #check for consistency and send OK response with IP of right Server who has DB.
    isConsistent = utilities.checkConsistency(clientIndex, indexFile)
    if(isConsistent is True):
        zk_client = C.KazooClient(hosts=serverIP)
        zk_client.start()
        lock = zk_client.Lock(dbName)
        lockAcquired = lock.acquire()

        #Maintain an entry in the DB for commit
        #probe all server for completion
        #if consistent state reached release the lock
        #return with success response


    print(serverIP,lockAcquired)
    if lock is not None:
        lock.release()
    #Else return Reject message
    return "Working Correctly"



@app.route("/rooot")
def hello():
    return "Hello World!"

@app.route("/signup")
def signup():
    return "signed UP"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)

