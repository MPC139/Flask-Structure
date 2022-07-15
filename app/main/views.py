from crypt import methods
from . import main
from flask import render_template, url_for, redirect
from datetime import datetime

@main.route('/')
def index():
    return render_template('index.html',current_time=datetime.utcnow())

@main.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name,current_time=datetime.utcnow())