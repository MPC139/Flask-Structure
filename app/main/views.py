from app.email import send_email
from . import main
from flask import render_template, url_for, redirect, flash, session, current_app
from datetime import datetime
from .forms import NameForm
from .. import db
from ..models import User,Role
from sqlalchemy.exc import IntegrityError
   


@main.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html',current_time=datetime.utcnow())


@main.route('/user/<username>')
def user(username):
    flash(f'Welcome {username}')
    return render_template('user.html',username = username,favorite_color = session['favorite_color'],current_time = datetime.utcnow())