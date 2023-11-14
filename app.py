import time
import os
from flask import Flask, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

import pyrebase

load_dotenv()

config = {
  'apiKey': os.getenv("API_KEY"),
  'authDomain': os.getenv("AUTH_DOMAIN"),
  'projectId': os.getenv("PROJECT_ID"),
  'storageBucket': os.getenv("STORAGE_BUCKET"),
  'messagingSenderId': os.getenv("MESSAGING_SENDER_ID"),
  'appId': os.getenv("APP_ID"),
  'measurementId': os.getenv("MEASUREMENT_ID"),
  'databaseURL': os.getenv("DATABASE_URL")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/time')
@cross_origin()
def get_current_time():
    return {'time': time.time()}

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    userInfo = request.get_json()
    newUser = auth.create_user_with_email_and_password(userInfo["email"], userInfo["password"])
    return {'User': newUser}

@app.route('/signin', methods=['POST'])
@cross_origin()
def signin():
    userInfo = request.get_json()
    loginUser = auth.sign_in_with_email_and_password(userInfo["email"], userInfo["password"])
    return {'User': loginUser}

@app.route('/signout', methods=['GET'])
@cross_origin()
def signout():
    auth.signOut()
    return {'Signed out'}

@app.route('/resetpassword', methods=['POST'])
@cross_origin()
def resetpassword():
    userInfo = request.get_json()
    passwordReset = auth.send_password_reset_email(userInfo["email"])
    return {'Password reset': passwordReset}

@app.route('/getUsers', methods=['GET'])
@cross_origin()
def get_users():
    users = db.child("users").get()
    return {'Users': users.val()}

@app.route('/checkEmail/<email>', methods=['GET'])
@cross_origin()
def check_email(email):
    users = db.child("users").get()
    user_data = users.val()

    if user_data:
        for user_id, user_info in user_data.items():
            if 'email' in user_info and user_info['email'] == email:
                return {'message': 'Email already in use'}, 400

    return {'message': 'Email is available'}, 200

@app.route('/getUser/<user_id>', methods=['GET'])
@cross_origin()
def get_user(user_id):
    users = db.child("users").child(user_id).get()
    return {'User': users.val()}

@app.route('/addUser/<user_id>', methods=['POST'])
@cross_origin()
def add_user(user_id):
    newUser = request.get_json()
    db.child("users").child(user_id).set(newUser)
    return {'New user': newUser}

@app.route('/updateUser/<user_id>', methods=['PUT'])
@cross_origin()
def update_user(user_id):
    user = request.get_json()
    db.child("users").child(user_id).update(user)
    return {'Updated user': user_id}

@app.route('/removeUser/<user_id>', methods=['DELETE'])
@cross_origin()
def delete_user(user_id):
    db.child("users").child(user_id).remove()
    return {'Removed user': user_id}

@app.route('/updateEvent/<event_id>', methods=['PUT'])
@cross_origin()
def update_event(event_id):
    event = request.get_json()
    db.child("events").child(event_id).update(event)
    return {'Updated event': event_id}

@app.route('/removeEvent/<event_id>', methods=['DELETE'])
@cross_origin()
def delete_event(event_id):
    db.child("events").child(event_id).remove()
    return {'Removed event': event_id}

@app.route('/getEvents', methods=['GET'])
@cross_origin()
def get_events():
    events = db.child("events").get()
    return {'Events': events.val()}

@app.route('/addEvent', methods=['POST'])
@cross_origin()
def add_event():
    newEvent = request.get_json()
    db.child("events").push(newEvent)
    return {'newEvent': newEvent}

@app.route('/addClub/<user_id>', methods=['POST'])
@cross_origin()
def add_club(user_id):
    newClub = request.get_json()
    db.child("clubs").child(user_id).set(newClub)
    return {'New club': newClub}

@app.route('/getClubs', methods=['GET'])
@cross_origin()
def get_clubs():
    clubs = db.child("clubs").get()
    return {'Clubs': clubs.val()}