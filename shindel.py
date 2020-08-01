import os
from flask import Blueprint, send_file, make_response, request, session, render_template, redirect, url_for
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