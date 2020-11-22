import os

from datetime import datetime
from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_session import Session

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize some chatrooms
chatroom = {}
chatroom['one'] = [('Hei folks, how are you doing?', '3 days ago', 'Alice'), ('Hi Alice, everything is alright here. Wbu', 'Yesterday', 'Fran'), ('Good thanks. Looking forwards to meeting you', '3 hours ago', 'Alice')]
chatroom['two'] = [('Who is up for a basketball game', '6:35 pm', 'Mark'), ('Sign me in', '6:47 pm', 'Nuria'), ('Got exams, see u next time', '7:01', 'Didac')]
chatroom['three'] = [('Need some help here', '5 hours ago', 'Marti'), ('Shoot, see what we can do', '3 hours ago', 'Louis'), ('3+8 = ?', '5 min ago', 'Marti')]
chatroom['four'] = []
# chatroom has 100 messages to test the scrolling down
for i in range(0, 100):
    message = []
    message.append(str(i))
    message.append('Yesterday')
    message.append('Aran')
    chatroom['four'].append(message)


# Index page function
@app.route("/")
def index():
    if 'username' in session:
        username = session['username']
        key_list = list(chatroom.keys())
        # for the index page the chatroom and user's name are needed
        return render_template("index.html", keys=key_list, user=username)
    # if user not logged in, redirect them to url_for
    return redirect(url_for('login'))


# Log in function needed to append the username to each message
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form.get("username")
        session['username'] = form_username
        return redirect(url_for('index'))
    return render_template("username.html")


# Log out function
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


#load messages from chatrooms
@app.route("/chat/<title>", methods=['GET', 'POST'])
def chatroom_funct(title):
    #return end-start messages to be added to the chat page
    if request.method == 'POST':
        start = int(request.form.get("start"))
        end = int(request.form.get("end"))
        data = chatroom[title][end:start]
        data.reverse()
        return jsonify(data)
    #load the 20 newest messages from the chatroom if exist
    else:
        messages = chatroom[title][len(chatroom[title]) - 20:len(chatroom[title])]
        user = session['username']
        room_length = len(chatroom[title])
        return render_template("chatroom.html", title=title, messages=messages, user=user, length=room_length)


#Delete a specific message from a chatroom
@app.route("/delete_message/", methods=['POST'])
def delete_message():
    msg = str(request.form.get("message"))
    room = str(request.form.get("room"))
    for i in range(len(chatroom[room]), 0, -1):
        if chatroom[room][i - 1][0] == msg:
            chatroom[room].pop(i - 1)
            return 'Message deleted correctly'


#add message and display it real time with socketio
@socketio.on("submit message")
def vote(data):
    selection = []
    selection.append(data["selection"])
    room = data["room"]
    selection.append(datetime.now().strftime('%d-%m-%Y %H:%M'))
    selection.append(session['username'])
    #only store 100 messages per chatroom, so delete oldest before adding a new one
    if (len(chatroom[room]) == 100): chatroom[room].pop(0)
    chatroom[room].append(selection)
    emit("announce message", {"selection": selection}, broadcast=True)

#Create a new chatroom and make it public for everyone
@socketio.on("create chatroom")
def create(data):
    new_chat = data["selection"]
    #chatrooms cannot have the same name
    if new_chat in list(chatroom.keys()):
        emit("announce chatroom", {"selection": "exists"}, broadcast=False)
    else:
        time = datetime.now().strftime('%d-%m-%Y %H:%M')
        chatroom[new_chat] = [('A new chatroom has been created', time)]
        emit("announce chatroom", {"selection": new_chat}, broadcast=True)
