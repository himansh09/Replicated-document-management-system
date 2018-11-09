from flask import Flask, render_template
from flask_socketio import SocketIO ,emit,send

import serverFunction

import sys
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on("pushDB")
def pullDB(message):
    serverFunction.pushDB(message)

@socketio.on("pullDB")
def pullDB(message):
    serverFunction.pullDB(message)

@socketio.on('connect')
def test_connect():
    print('my response', {'data': 'Connected'})

@socketio.on('copySuccess')
def copySuccess():
    #insert DB entry and modify lock to 0
    print(1)

@socketio.on('replicate')
def replicate(message):
    print("start replication")


@socketio.on('checkConsistency')
def handle_message(message):
    print(message,sys.stdout)
    emit("consistent",{"Hel":"Iemted"})



if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0",port=8000,debug=True)


