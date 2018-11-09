from socketIO_client import SocketIO

def pushToRemoteServer(*args):
    serverIP = args[0]
    db_name_to_pull = "db1"  ##will be read
    client_prefix = "/Source/ClientTest"
    print("hel")

def ifNotConsistent(*args):
    print("Please pull the DB first and then try to commit");
    socketIO.disconnect()

with SocketIO('172.17.0.8', 80) as socketIO:
    socketIO.on("notConsistent", ifNotConsistent)
    socketIO.on("pushSignal",)
    socketIO.wait()
    socketIO.disconnect()