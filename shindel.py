import os
from flask import Blueprint, send_file, make_response, request, session, render_template, redirect, url_for, abort
import json
from helper import from_log,update_log,sessionvalidated,next_element,del_log
import json
import base64

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
        if "loggedIn" in session and session["loggedIn"] == True:
            return redirect(url_for("ui.home"))
        else:
            return render_template("login.html")

@ui.route('/')
@sessionvalidated
def home():
    return render_template("main.html")

@ui.route('/<lang>/announcements',methods=["GET","POST"])
@sessionvalidated
def announcements(lang):
    start=int(request.args.get('start',0))
    announcementlog=json.loads(from_log('data/'+lang+'/announcements',0,'end'))['data']
    if start < 0:
        start = 0
    elif start >= len(announcementlog):
        start = len(announcementlog)-len(announcementlog)%5
    if request.method == "GET":
        return render_template('announcements.html',start=start,names=announcementlog[start:start+5],lang=lang)
    elif request.method == "POST":
        name = next_element(lang,'announcements')
        content = json.dumps(dict(request.form))
        with open('data/'+lang+'/announcements/'+name,'w') as f:
            f.write(content)
        announcementlog.insert(0,dict(request.form))
        update_log('data/'+lang+'/announcements',name)
        return render_template('announcements.html',start=start,names=announcementlog[start:start+5],lang=lang)

@ui.route('/<lang>/announcements/del',methods=["POST"])
@sessionvalidated
def delannounce(lang):
    announcement=json.loads(from_log('data/'+lang+'/announcements',0,'end'))['data'][int(request.form['num'])]
    if str(announcement) == str(request.form['value']):
        del_log('data/'+lang+'/announcements',int(request.form['num']))
        return redirect(url_for("ui.announcements",lang=lang))
    else:
        return "Please do not use this API incorrectly"

@ui.route('/<lang>/events',methods=["GET","POST"])
@sessionvalidated
def events(lang):
    start=int(request.args.get('start',0))
    eventlog=json.loads(from_log('data/'+lang+'/events',0,'end'))['data']
    if start < 0:
        start=0
    elif start >= len(eventlog):
        start = len(eventlog)-len(eventlog)%5
    if request.method == "GET":
        return render_template('events.html',events=eventlog[start:start+5],lang=lang,start=start)
    elif request.method == "POST":
        name = next_element(lang,'events')
        content = json.dumps(dict(request.form))
        with open('data/'+lang+'/events/'+name,'w') as f:
            f.write(content)
        eventlog.insert(0,dict(request.form))
        update_log('data/'+lang+'/events',name)
        return render_template('events.html',events=eventlog[start:start+5],lang=lang,start=start)

@ui.route('/<lang>/events/del',methods=["POST"])
@sessionvalidated
def delevent(lang):
    event=json.loads(from_log('data/'+lang+'/events',0,'end'))['data'][int(request.form['num'])]
    if str(event) == str(request.form['value']):
        del_log('data/'+lang+'/events',int(request.form['num']))
        return redirect(url_for("ui.events",lang=lang))
    else:
        return "Please do not use this API incorrectly"

@ui.route('<lang>/new',methods=["GET","POST"])
@sessionvalidated
def new(lang):
    start=int(request.args.get('start',0))
    newlog=json.loads(from_log('data/'+lang+'/new',0,'end'))['data']
    if start < 0:
        start=0
    elif start >= len(newlog):
        start = len(newlog)-len(newlog)%5
    if request.method == "GET":
        return render_template('new.html',news=newlog[start:start+5])
    else:
        name = next_element(lang,'new')
        content = {
            'icon':base64.b64encode(request.files['icon'].read()).decode(),
            'name':request.form['name'],
            'date':request.form['date']
        }
        with open('data/'+lang+'/new/'+name,'w') as f:
            f.write(json.dumps(content))
        update_log('data/'+lang+'/new',name)
        newlog.insert(0,content)
        return render_template('new.html',news=newlog[start:start+5])
