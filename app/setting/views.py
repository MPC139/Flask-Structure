from crypt import methods
from lib2to3.pgen2 import token
from flask import render_template,redirect , url_for,flash, current_app,request,session
from flask_login import login_user, logout_user,login_required, current_user
from .forms import ChangePassword, ChangeEmail, ResetPassword_step_1, ResetPassword_step_2
from . import setting
from .. import db
from ..models import User
from ..email import send_email


@setting.route('/', methods = ['GET','POST'])
@login_required
def index():
    form = ChangePassword()
    form2 = ChangeEmail()

    if form.validate_on_submit():
        if current_user.verify_password(form.actual_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            form.actual_password.data = ''
            form.new_password.data = ''
            form.new_password2.data = ''
            flash('You have changed password.')
        else:
            form.actual_password.data = ''
            form.new_password.data = ''
            form.new_password2.data = ''
            flash('You have entered wrong password.')
    if form2.validate_on_submit():
        if current_user.verify_password(form2.password.data):
            current_user.email = form2.new_email.data 
            current_user.confirmed = False
            db.session.add(current_user)
            db.session.commit()
            form2.new_email.data = ''
            form2.new_email2.data = ''
            form2.password.data = ''
            form2.password2.data= ''
            flash('You have updated your email. Please verify your new email to confirm.')
        else:
            form2.new_email.data = ''
            form2.new_email2.data = ''
            form2.password.data = ''
            form2.password2.data= ''
            flash('You have entered wrong email or password.')

    return render_template('setting/index.html',form = form,form2 = form2)


@setting.route('/reset',methods=['GET','POST'])
def reset():
    form = ResetPassword_step_1()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            flash('The email you entered does not exist.')
        else:
            token = user.generate_confirmation_token(expiration=120)
            send_email(user.email,'Reset Your Password',
                                'setting/reset_pass/reset',user = user, token = token)
            return redirect(url_for('auth.login'))
    return render_template('setting/reset_step_1.html',form = form)
    

@setting.route('/confirm/<token>/<user_email>',methods = ['GET','POST'])
def confirm(token,user_email):
    form = ResetPassword_step_2()
    user = User.query.filter_by(email = user_email).first()
    if user.confirm(token) and user is not None:
        if form.validate_on_submit():
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash("You have reset your password.")
            return redirect(url_for('auth.login'))
        return render_template('setting/reset_step_1.html',form = form)
    return render_template('404.html')