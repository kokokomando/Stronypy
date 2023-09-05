import mailbox
from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from .models import Note, rooms
from . import db
import json
import random
from string import ascii_uppercase
from flask_socketio import SocketIO, send, join_room, leave_room
import os

views = Blueprint('views', __name__)

def generate_unique_code(length):
    directory_path = './website/uploads'
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        

        if code not in rooms: # spradzanie czy już nie jest
            break

        if code not in os.listdir(directory_path):
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

@views.route('/wzory', methods=['GET'])
def wzory():
    
            

    return render_template("wzory.html", user=current_user)


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



@views.route('/upload', methods=['POST'])
def upload_file():
    AUTH_KEY = '12345'
    room = request.headers.get('room')
   
    UPLOAD_FOLDER2 = f'website/uploads/{room}'
    
 

    if not os.path.exists(UPLOAD_FOLDER2):
        os.makedirs(UPLOAD_FOLDER2) # do naprawienia bo return filesend wykyrwa inaczej xddd i trzeba 2x ??


    # Check if the authentication key is present in the POST request
    auth_key = request.headers.get('auth')
    
    if auth_key != AUTH_KEY:
        return jsonify({'error': 'Authentication failed'}), 401

    # Check if a file is included in the POST request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file to the uploads directory


    
    file_path = os.path.join(UPLOAD_FOLDER2, file.filename)
    file.save(file_path)

    # Generate the URL for downloading the uploaded file
    download_url = request.host_url + file_path

    return jsonify({'message': 'File uploaded successfully', 'download_url': download_url}), 200



@views.route('/download_files', methods=['POST', 'GET'])
def download_files():

    if request.method == "POST":
        # Get the folder name from the POST request
        folder_name = request.form.get('folder_name')
        UPLOAD_FOLDER = f'uploads/{folder_name}'
        
        print(folder_name)

        if not folder_name:
            return jsonify({'error': 'Folder name not provided in the POST request'}), 400

        # Specify the base directory where the folders are located
        base_directory = 'uploads'  # Adjust this path to your needs

        # Construct the full path to the specified folder
        folder_path = os.path.join("website", UPLOAD_FOLDER)

        # Check if the folder exists
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return jsonify({'error': 'Folder not found'}), 404

        # List all files in the specified folder
        files = os.listdir(folder_path)

        # Check if there are any files in the folder


        # Create a ZIP file to contain all the files
        zip_filename = f'{folder_name}_files.zip'
        zip_filepath = os.path.join("website", UPLOAD_FOLDER, zip_filename)

        # Create the ZIP file
        import zipfile
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                zipf.write(zip_filepath, os.path.basename(file_path))

        
        print("Wysyłam PLIK XDDDDD")    # Use Flask's send_from_directory function to send the ZIP file to the client
        print(file_path)
        print(zip_filename)
        print(zip_filepath)
        return send_from_directory(UPLOAD_FOLDER, zip_filename, as_attachment=True)
    else:
        return send_from_directory("./static/", "firmowy.dotx", as_attachment=True)
        





