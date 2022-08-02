from flask import render_template,redirect , url_for,flash, current_app
from flask_login import login_user, logout_user
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import send_email

@auth.route('/login',methods = ['GET','POST'] )
def login():
    form = LoginForm()
    if form.is_submitted():
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(url_for('main.index'))
        flash('Invalid Username or Password')
    form.email.data = ''
    form.password.data = ''
    return render_template('auth/login.html',form = form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.is_submitted():
        user = User(username = form.username.data,
                         email = form.email.data,
                         password = form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email(current_app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
        flash('You can now Login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form = form)