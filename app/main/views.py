from . import main
from flask import render_template, url_for, redirect, flash, session
from datetime import datetime
from .forms import NameForm
from .. import db
from ..models import User,Role

# @main.route('/',methods=['GET','POST'])
# def index():
#     form = NameForm()
#     name = None
#     password = None
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#         form.password.data = ''
#         return redirect(url_for('main.user',name=name))
#     elif form.name.data!=None or form.password.data!=None:
#         flash("Looks like you have put invalid name o password")
#         form.name.data = ''
#         form.password.data = ''
#     return render_template('index.html',current_time=datetime.utcnow(),form=form)

@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.user.data, password = form.password.data).first()
        if user == None:
            flash("Username is not registered.")
            form.user.data = ''
            form.password.data = ''
            return render_template('index.html',current_time=datetime.utcnow(),form = form)
        name = form.user.data
        form.user.data = ''
        form.password.data = ''
        return redirect(url_for('main.user',name=name))
    return render_template('index.html',current_time=datetime.utcnow(),form = form)


@main.route('/user/<name>')
def user(name):
    flash(f'Welcome {name}')
    return render_template('user.html',name=name,current_time=datetime.utcnow())