from crypt import methods
from tokenize import Name
from unicodedata import name
from . import main
from flask import render_template, url_for, redirect, flash, session
from datetime import datetime
from .forms import NameForm

@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    name = None
    password = None
    if form.validate_on_submit() and form.password.data == '1234':
        name = form.name.data
        form.name.data = ''
        form.password.data = ''
        return redirect(url_for('main.user',name=name))
    elif form.name.data!=None or form.password.data!=None:
        flash("Looks like you have put invalid name o password")
        form.name.data = ''
        form.password.data = ''
    return render_template('index.html',current_time=datetime.utcnow(),form=form)

@main.route('/user/<name>')
def user(name):
    flash('Welcome')
    return render_template('user.html',name=name,current_time=datetime.utcnow())