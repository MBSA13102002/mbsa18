from flask import Flask,render_template

from firebase import Firebase
config = {
    "apiKey": "AIzaSyDO2W0QCmFCo0a-PTsT7ficA_QLI5e_WHg",
    "authDomain": "chat-a7bab.firebaseapp.com",
    "databaseURL": "https://chat-a7bab-default-rtdb.firebaseio.com",
    "projectId": "chat-a7bab",
    "storageBucket": "chat-a7bab.appspot.com",
    "messagingSenderId": "550345253145",
    "appId": "1:550345253145:web:c6f493380c62bed2d02588",
    "measurementId": "G-R8DG3WGW88"
  };

app = Flask(__name__)
firebase = Firebase(config)
db = firebase.database()

@app.route("/",methods= ['GET','POST'])
def start():
    key = db.generate_key()
    return render_template("index.html",key = key)

