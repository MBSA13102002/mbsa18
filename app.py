
from flask import Flask,render_template,request,g,url_for,redirect,make_response
import os
import json,time
from firebase import Firebase
config = {
    "apiKey": "AIzaSyDZz8e_QIruwWnyOclDfnPQEjKvCQEZ1GE",
    "authDomain": "nitk-attendance.firebaseapp.com",
    "databaseURL": "https://nitk-attendance-default-rtdb.firebaseio.com",
    "projectId": "nitk-attendance",
    "storageBucket": "nitk-attendance.appspot.com",
    "messagingSenderId": "911144952264",
    "appId": "1:911144952264:web:37ab1feabfe1927bc5e0fd",
    "measurementId": "G-V3LM0Y97FC"
  };

firebase = Firebase(config)
db = firebase.database()


app = Flask(__name__)
app.secret_key = os.urandom(24)

def handle_catch(caller, on_exception):
    try:
         return caller()
    except:
         return on_exception



@app.route("/",methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        uname = request.form.get("username")     
        resp = make_response(render_template("dashboard.html",handle_catch = handle_catch ))
        verified = db.child("Users").child(uname).child("verified").get().val()
        if(verified!=1):
            resp.set_cookie('__key__', uname)
            db.child("Users").child(uname).update({
                'verified':1
            })
            return resp
        else:
            return f"User {uname} Already Verfied with some other device!!"
            


    if request.cookies.get('__key__')is not None:
        resp = make_response(render_template("dashboard.html",handle_catch = handle_catch))
        resp_err = make_response("You Are not the Verified!!!")
        verified = db.child("Users").child(request.cookies.get('__key__')).child("verified").get().val()
        if(verified==1):
            return resp
        else:
            return resp_err

    return render_template("index.html")

@app.route("/verify",methods = ['GET','POST'])
def verify():
    if request.method == 'POST':
        value = request.get_json()
        db.child("_Attendance_").child(value['key']).set({
            'RollNo':request.cookies.get('__key__'),
            "datetime":value['date'],
            "verified":1
        })
        
    return render_template("success.html")










