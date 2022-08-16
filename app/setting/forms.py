from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,Email,EqualTo


class ChangePassword(FlaskForm):
    actual_password = PasswordField('Actual Password',validators=[Required()])
    new_password = PasswordField('New Password',validators=[Required(),EqualTo('new_password2',message="Password must match.")])
    new_password2 = PasswordField('Repeat New Password',validators=[Required()])
    submit = SubmitField('Update Password')

class ChangeEmail(FlaskForm):
    new_email = StringField('New Email',validators=[Email(),Required(),EqualTo('new_email2',message='Email must match.')])
    new_email2 = StringField('Repeat New Email',validators=[Required()])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message="Password must match.")])
    password2 = PasswordField('Repeat Password',validators=[Required()])
    submit = SubmitField('Update Email')
    
class ResetPassword_step_1(FlaskForm):
    email = StringField('Email',validators=[Email(),Required()])
    submit = SubmitField('Reset Password')

class ResetPassword_step_2(FlaskForm):
    new_password = PasswordField('New Password',validators=[Required(),EqualTo('new_password2',message="Password must match.")])
    new_password2 = PasswordField('Repeat New Password',validators=[Required()])
    submit = SubmitField('Reset Password')