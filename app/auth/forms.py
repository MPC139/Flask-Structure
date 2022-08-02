from ast import Pass
from email.message import EmailMessage
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import Required,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from ..models import User



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[Email(),Required(),Length(1,40)])
    password = PasswordField('Password:',validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
                                                                                'Usernames must have only letters,'
                                                                                'number, dots or underscores')])
    password = PasswordField('Password',validators=[Required(),EqualTo('password2',message='Password must match.')])
    password2 = PasswordField('Confirm password',validators=[Required()])
    submit = SubmitField('Register')

    # When a form defines a method with the prefix 'validate_' followed by the name of a field, the method is invoked in addition to any
    # regularly defined validators. 
    # In this case the custom validators for email and username ensure that the values given are not duplicates rising an error if the mentioned
    # comes true.
    def validate_email(self,field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already registered.')
    