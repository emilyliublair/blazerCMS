import os
from flask import Blueprint, send_file, make_response, request, session, render_template, redirect, url_for
import json
from helper import from_log,update_log
import json

ui = Blueprint('ui', __name__, url_prefix='/ui')

@ui.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        important = json.load(open("important.json"))
        if username == important["shindelUsername"] and password == important["shindelPassword"]:
            session["loggedIn"] = True
        else: 
            session["loggedIn"] = False
        return redirect(url_for("ui.home"))
    elif request.method  == "GET":
        return render_template("login.html")


@ui.route('/')
def home():
    if "loggedIn" not in session:
        return "You are not logged in"
    elif session["loggedIn"] == False:
        return "You are not logged in"
    else: 
        return render_template("main.html")

@ui.route('/<lang>/announcements',methods=["GET","POST"])
def announcements(lang):
    if 'loggedIn' not in session:
        return "You are not logged in"
    elif session["loggedIn"] == False:
        return "You are not logged in"
    else:
        announcelog=json.loads(from_log('data/'+lang+'/announcements',0,'end'))
        names = [x['message'] for x in announcelog['data']]
        if request.method == "GET":
            return render_template('announcements.html',names=names)
        elif request.method == "POST":
            name = 'announcement'+str(len(announcelog['data']))+'.json'
            content = json.dumps(dict(request.form))
            with open('data/'+lang+'/announcements/'+name,'w') as f:
                f.write(content)
            names.insert(0,request.form['message'])
            update_log('data/'+lang+'/announcements',name)
            return render_template('announcements.html',names=names)

@ui.route('/<lang>/events',methods=["GET","POST"])
def events(lang):
    if 'loggedIn' not in session:
        return "You are not logged in"
    elif session["loggedIn"] == False:
        return "You are not logged in"
    else:
        events=json.loads(from_log('data/'+lang+'/events',0,'end'))['data']
        if request.method == "GET":
            return render_template('events.html',events=events)
        elif request.method == "POST":
            name = 'event'+str(len(events))+'.json'
            content = json.dumps(dict(request.form))
            with open('data/'+lang+'/events/'+name,'w') as f:
                f.write(content)
            events.insert(0,dict(request.form))
            update_log('data/'+lang+'/events',name)
            return render_template('events.html',events=events)
