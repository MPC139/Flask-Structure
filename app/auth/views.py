from flask import render_template,redirect , url_for,flash, current_app,request
from flask_login import login_user, logout_user,login_required, current_user
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')

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
@login_required
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
        try:
            db.session.commit()
        except:
            flash('email or username is registered already.')
            db.session.rollback()
            form.email.data = ''
            form.username.data = ''
            form.password.data = ''
            form.password2.data = ''
        else:
            token = user.generate_confirmation_token()
            send_email(current_app.config['FLASKY_ADMIN'], 'New User','mail/new_user', user=user)
            send_email(user.email,'Confirm Your Account',
                                    'auth/email/confirm',user = user, token = token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html',form = form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account',
                'auth/email/confirm',user = current_user, token = token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))