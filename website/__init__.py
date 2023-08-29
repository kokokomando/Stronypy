from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from flask import session 


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    socketio = SocketIO(app)
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, rooms
    
   
    @socketio.on("connect")
    def connect(auth):
        auth_key = request.headers.get('auth')
        
        if auth_key == '12345':
            print("jest Auth Good :D")
            print(request.headers.get('room'))
            room = request.headers.get('room')
            name = request.headers.get('name')
            rooms[room] = {"members": 0, "messages": []}
        else:
            room = session.get("room")
            name = session.get("name")
        
        if room not in rooms:
            print(f"{room} not in Rooms")
            return
            

        join_room(room)
        if room == '4441':
            BartekCzeka = True
            print("BartekCzekaTrue")

        send({"name": name, "message": "has entered the room"}, to=room)
        send({"name": name, "message": f"{name} has entered the room *{room}*"}, to="4441")
        rooms[room]["members"] += 1
        print(f"{name} joined room {room}")

    @socketio.on("disconnect")
    def disconnect():
        auth_key = request.headers.get('auth')

        if auth_key == '12345':
            room = request.headers.get('room')
            name = request.headers.get('name')
        else:
            room = session.get("room")
            name = session.get("name")
        
        
        leave_room(room)
        if room == '4441':
            BartekCzeka = False
            print("BartekCzekaFalse")
            for room_name in rooms.keys():
                send({"message": "Bartek Left"}, to=room_name)

        if room in rooms:
            rooms[room]["members"] -= 1
            if rooms[room]["members"] <= 0 or name == "2_Bartek":
                del rooms[room]
                send({"message": "The room has been deleted because Bartek left"}, to=room)
                print(f"{name} has left the room {room}, and the room has been deleted.")
                print("Room codes after deleting a room:", list(rooms.keys()))
                print("KONIEC")
    
        send({"name": name, "message": "has left the room"}, to=room)
        send({"name": name, "message": f"has left the room {room}"}, to="4441")
        print("Room codes after deleting a room:", list(rooms.keys()))
        print(f"{name} has left the room {room}")


    @socketio.on("message")
    def message(data):
        auth_key = request.headers.get('auth')
        
        if auth_key == '12345':
            
            print(request.headers.get('room'))
            room = request.headers.get('room')
            
        else:
            
            room = session.get("room")
        
        if room not in rooms:
            print(f"{room} not in Rooms")
            return
            

        if auth_key == '12345':
            content = {
                "name": request.headers.get('name'),
                "message": data.get('message', '')
            }
            
            ContentMessage = content["message"]
            ContentName = content["name"]
            if ContentMessage.count("#") == 2 and ContentName == "2_Bartek" :
                start_index = ContentMessage.index("#") + 1
                end_index = ContentMessage.rindex("#")
                room = ContentMessage[start_index:end_index]

        
            
            send(content, to=room)
            rooms[room]["messages"].append(content)
            print(content)

        else:
            content = {
                "name": session.get("name"),
                "message": data["data"] + f", @{room}@"  # Use data.get() to safely access the message
            }
            send(content, to=room)
            send(content, to="4441")
            rooms[room]["messages"].append(content)
            print(f"{session.get('name')} said: {data['data']} @{room}@")    
 



    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app, socketio


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')




 
