from . import main
from flask import render_template, url_for, redirect, flash, session
from datetime import datetime
from .forms import NameForm
from .. import db
from ..models import User,Role
from sqlalchemy.exc import IntegrityError   


@main.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.user.data, password = form.password.data).first()
        if user == None:
            flash("Username is not registered.")
            user = User(username = form.user.data, password = form.password.data, favorite_color = form.favorite_color.data, role = Role.query.filter_by(name = 'user').first())
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                flash("Username registered. Try with other username.")
            else:
                flash("Username has been registered. Try to log.")
            finally:
                form.user.data = ''
                form.password.data = ''
                form.favorite_color.data = ''
                return render_template('index.html',current_time=datetime.utcnow(),form = form)
        else:
            username = form.user.data
            if form.favorite_color.data:
                user.favorite_color = form.favorite_color.data
                session['favorite_color'] = user.favorite_color
            else:
                if user.favorite_color:
                    session['favorite_color'] = user.favorite_color
                else:
                    session['favorite_color'] = None
                    
            db.session.add(user)
            db.session.commit()
            form.user.data = ''
            form.password.data = ''
            form.favorite_color.data = ''
            return redirect(url_for('main.user',username=username))
    return render_template('index.html',current_time=datetime.utcnow(),form = form)


@main.route('/user/<username>')
def user(username):
    flash(f'Welcome {username}')
    return render_template('user.html',username = username,favorite_color = session['favorite_color'],current_time = datetime.utcnow())