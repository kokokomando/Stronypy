import socketio
import time
import re

sio = socketio.Client()



@sio.on('message')
def on_message(data):


    name = data.get('name', 'Unknown')
    message = data.get('message', '')
    print(f"{name}: {message}")
    roomSearch = re.search(r'\*(.*?)\*', message)
    
    if roomSearch:
        room = roomSearch.group(1)
        if room != "4441":
            print("New Room:", room)
            current_room = room  # Update the current room
            message1 = {"name": "2_Bartek", "message": f"elo420#{room}#"}
            sio.emit('message', message1)
    else:
        
        if "%" in message:
            print("jest %")
            substrings = message.split(", ")
            print(substrings)
            email = substrings[0].replace("%", "")
            znak = substrings[1].replace("%", "")
            numer = substrings[2].replace("%", "")
            umowa = substrings[3].replace("%", "")
            room = substrings[4].replace("@", "")
            print(room, email, znak, numer, umowa)
            
            message2 = {"name": "2_Bartek", "message": f"jestem#{room}#"}
            sio.emit('message', message2)
        else:
            print("No Room found in the string.")

@sio.on('connect')
def on_connect():
    print('Connected to chatroom')
    time.sleep(2)
    message1 = {"name": "2_Bartek", "message": "elo420"} 
    sio.emit('message', message1)

@sio.on('disconnect')
def on_disconnect():
    print('Disconnected from chatroom')



headers = {'auth': '12345', 'room': '4441', 'name': '2_Bartek'}


print(headers)

# Replace 'https://chatroom-website-url.com' with the actual URL of the chatroom
sio.connect('http://127.0.0.1:5000', headers=headers)

sio.wait()
