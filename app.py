
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
            resp.set_cookie('__key__', uname,max_age=60*60*24)
            db.child("Users").child(uname).update({
                'verified':1
            })
            return resp
        else:
            return f"User {uname} Already Verfied with some other device!!"
            


    if request.cookies.get('__key__')is not None:
        resp = make_response(render_template("dashboard.html",handle_catch = handle_catch))
        verified = db.child("Users").child(request.cookies.get('__key__')).child("verified").get().val()
        if(verified==1):
            return resp
        else:
            return "You Are not the Verified!!!"

    return render_template("index.html")

@app.route("/verify",methods = ['GET','POST'])
def verify():
    global success
    success = 0
    if request.method == 'POST':
        success = 0
        value = request.get_json()
        all_entries = db.child("_Attendance_").get().val()
        if(all_entries!=None):
            if(value['key'] not in all_entries.keys()):
                db.child("_Attendance_").child(value['key']).set({
                    'RollNo':request.cookies.get('__key__'),
                    "datetime":value['date'],
                    "verified":1
                })
                print("success")
                success = 1
            else:
                success = 0
        else:
            db.child("_Attendance_").child(value['key']).set({
                    'RollNo':request.cookies.get('__key__'),
                    "datetime":value['date'],
                    "verified":1
                })
            success = 1
    if (success==1):
        return render_template("success.html")
    else:
        return render_template("danger.html")


            
    










