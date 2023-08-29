import mailbox
from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, rooms
from . import db
import json
import random
from string import ascii_uppercase
from flask_socketio import SocketIO, send, join_room, leave_room

views = Blueprint('views', __name__)

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code




@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("chose.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})




@views.route('/wybierz', methods=['GET'])
def wybierz():
   
    return render_template("chose.html", user=current_user)



@views.route('/wybierz1', methods=['GET'])
def wybierz1():
   
    return render_template("chose copy.html", user=current_user)




@views.route('/przedwstepna', methods=['GET'])
def przedwstepna():
   
    return render_template("przedwstepna.html", user=current_user)


@views.route('/darowizna', methods=['GET'])
def darowizna():
   
    return render_template("darowizna.html", user=current_user)


@views.route('/najem', methods=['GET'])
def najem():
   
    return render_template("najem.html", user=current_user)







@views.route("/umowa", methods=["POST", "GET"])
def chatHome():
    session.clear()
    if request.method == "POST":
        if current_user.is_authenticated:
            
            name = f"{current_user.id}_{current_user.first_name}"
            email = current_user.email
            
        else:
            email = ""
            name = "Niezal"
                   
        RodzajUmowy = request.form.get("RodzajUmowy")
        room = generate_unique_code(4)
        rooms[room] = {"members": 0, "messages": []}
        print("Room codes after adding a new room:", list(rooms.keys()))
               
        rooms[room] = {"members": 0, "messages": []}
        

        session["RodzajUmowy"] = RodzajUmowy
        session["email"] = email
        session["room"] = room
        session["name"] = name

        return redirect(url_for("views.room", room = room))

    return redirect(url_for("views.wybierz"))



@views.route("/room", methods=["POST", "GET"])
def room():
    
    email = session.get("email")
    room = session.get("room")
    RodzajUmowy = session.get("RodzajUmowy")
    name = session.get("name")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("views.wybierz"))

    return render_template("umowa.html",  RodzajUmowy = RodzajUmowy, messages=rooms[room]["messages"],  user=current_user, name=name, email=email, room=room)



        





