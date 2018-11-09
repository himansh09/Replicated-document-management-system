from socketIO_client import SocketIO
import fetch_files
import os

def pullSignal(*args):
    serverIP = args[0]
    db_name_to_fetch = "db1" ##will be read
    client_prefix = "/Source/ClientTest"
    
    folders_to_fetch = [os.path.join(db_name_to_fetch,'.mvc/master')]
    files_to_fetch = [os.path.join(db_name_to_fetch,'.mvc/index.json')]
    
    
    
    #Himanshu Insert your code here
    fetch_files.fetch_folder(serverIP,folders_to_fetch,client_prefix)
    os.rename(os.path.join(db_name_to_fetch,'./mvc/index.json'),os.path.join(db_name_to_fetch,'./mvc/index_old.json'))
    fetch_files.fetch_files(serverIP,files_to_fetch,client_prefix)
    socketIO.disconnect()

with SocketIO('172.17.0.8', 80) as socketIO:
    socketIO.emit("pullDB", {"dbName": "db1"})
    socketIO.on("pullSignal", pullSignal)
    socketIO.wait()