# pull and merge mvc
import os
import sys
import pprint
import json
import MVCMeta
import MVC
import re
import time
import init
from socketIO_client import SocketIO
import fetch_files
import os
myEncoder = lambda o:o.__dict__


def pullSignal(*args):
    global m,dbName,rp,timeout
    #Ip of the serverfrom which the DB has to be pulled
    serverIP = args[0]
    #DB to be pulled from the server
    db_name_to_fetch = dbName
    client_prefix = m.getRepoPath() + '/.mvc'
    remotePrefix= "/Source/Repo/" + dbName + '/.mvc'
    folders_to_fetch = ['master']
    files_to_fetch = ['index.json']
    os.rename(os.path.join(rp, '.mvc/index.json'),os.path.join(rp, '.mvc/old_index.json'))
    fetch_files.fetch_files(serverIP, files_to_fetch, client_prefix,remotePrefix)
    fetch_files.fetch_folder(serverIP,folders_to_fetch,client_prefix,remotePrefix)
    index = open(rp + '/.mvc/index.json', 'r+')
    newIndexData = json.load(index)
    newIndexData['repoPath'] = rp
    index.seek(0)
    index.truncate()
    json.dump(newIndexData,index)
    index.close()
    timeout = False
    socketIO.disconnect()


if __name__=='__main__':
    domainIP = '172.17.0.8'
    domainPort = 80
    rp = init.mvcInit()
    m = MVC.MVC(repoPath=rp)
    dbName = m.getDbName()
    flag = 1
    timeout = True
    print("Connecting to Server", sys.stdout)
    sys.stdout.flush()
    while flag < 6 :
        try:
            with SocketIO(domainIP, domainPort,wait_for_connection=False) as socketIO:
                    socketIO.emit("pullDB", {"dbName": dbName})
                    socketIO.on("pullSignal", pullSignal)
                    socketIO.wait()
                    if not timeout :
                        m.mergeWithLatestVersion()
                        os.remove(os.path.join(rp, '.mvc/old_index.json'))
                        flag = 6
                    else:
                        flag = flag + 1
        except:
            print("Reconnecting to Server")
            time.sleep(3)
            sys.stdout.flush()
            flag = flag + 1
    if not timeout:
        print("Pull Successful")
        sys.stdout.flush()
    else:
        print("Server down please retry later")
        sys.stdout.flush()

    pass