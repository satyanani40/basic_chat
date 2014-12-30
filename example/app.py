from gevent import monkey
from models import users,chatrooms,messages
from mongoengine import connect
import json
from flask import abort, redirect, url_for,session
monkey.patch_all()
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, join_room, leave_room
from mongoengine.base import BaseDocument
import datetime
from mongoengine.queryset import Q
from flask.ctx import copy_current_request_context

connect('test')

app = Flask(__name__)


app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

def check_messages_came(username):
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        time.sleep(10)
        print 'thread running'
        data =  messages.objects( Q(user2=username) & Q(transfered_data=False))
        if data:
            socketio.emit('my response',{'data': 'some messages are got', 'count': count},
                          namespace='/test')
        else:
            socketio.emit('my response',{'data': 'no message to read', 'count': count},
                          namespace='/test')

        count += 1




@app.route('/')
def index():
    return render_template('index2.html')

class MongoengineObjectsJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BaseDocument):
            return o._data
        elif isinstance(o, datetime):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)

@app.route('/home')
def home():
    users_list = []

    if session['username'] != '':
        data = users.objects(username__ne=session['username'])
        for user in data:
            users_list.append(user.username)
        #s_data = json.dumps(data, cls=MongoengineObjectsJsonEncoder)
        global thread
        if thread is None:
            #thread = Thread(target=check_messages_came(session['username']))
            #thread.start()
            print 'hai'

        return render_template('home.html',data=(users_list),me = session['username'])



    else:
        return redirect(url_for('login'))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.form['username'] != '':
            try:
                data = users.objects.get(username = request.form['username'])
                session['username'] = request.form['username']
                return redirect(url_for('home'))

            except Exception as e:
                return 'invalied username %s' %e

        else:
            return 'please enter user name'

    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            if request.form['username'] != '':
                user = users(username=request.form['username'])
                user.save()
                return redirect(url_for('login'))
            else:
                return 'please enter username'
        except Exception as e:

            return 'username alredy exits %s' %e

    else:
        return render_template('register.html')

"""@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})"""



@socketio.on('join', namespace='/test')
def join(message):
    if message['room'] != '':
        data = str.split(str(message['room']),"_")
        myname = data[1]
        partnername = data[0]

        data = chatrooms.objects( (Q(user1=myname) & Q(user2=partnername)) | (Q(user1=partnername) & Q(user2=myname)))
        # print data[0]
        if data:
            join_room(str(data[0].chat_room_name))
            print 'joined in =='+str(data[0].chat_room_name)
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my response',
                 {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
                  'count': session['receive_count']})
        else:
            insert_rm = chatrooms(user1 = myname, user2= partnername,chat_room_name= myname+"_"+partnername)
            insert_rm.save()
            print 'created and joined '
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my response',
                 {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
                  'count': session['receive_count']})




@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': 'In rooms: ' + ', '.join(request.namespace.rooms),
          'count': session['receive_count']})


@socketio.on('my room event', namespace='/test')
def send_room_message(message):
    if message['room'] != '':
        data = str.split(str(message['room']),"_")
        myname = data[1]
        partnername = data[0]
        data = chatrooms.objects( (Q(user1=myname) & Q(user2=partnername)) | (Q(user1=partnername) & Q(user2=myname)))

        if data:
            print data[0].chat_room_name
            session['receive_count'] = session.get('receive_count', 0) + 1
            emit('my response',{'data': message['data'], 'count': session['receive_count']},room=data[0].chat_room_name)
            try:
                insert_message = messages(user1 = myname, user2 = partnername, message = message['data'], created= datetime.datetime.now())
                insert_message.save()
            except Exception as e:
                print e
        else:
            print 'sending failed'

"""@socketio.on('connect', namespace='/test')
def test_connect():

    emit('my response', {'data': 'Connected', 'count': 0})"""


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
