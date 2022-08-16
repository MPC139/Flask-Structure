from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,TextAreaField,BooleanField
from wtforms.validators import Required,Length,Email,Regexp,ValidationError
from ..models import Role,User

class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(1,64)])
    location = StringField('Location', validators=[Length(1,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email',validators=[Required(),Length(1,64),Email()])
    username = StringField('Username',validators=[
        Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                'Usernames must have only letters, '
                                'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    name = StringField('Real name',validators=[Length(0,64)])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user


    # When a form defines a method with the prefix 'validate_' followed by the name of a field, the method is invoked in addition to any
    # regularly defined validators. 
    # In this case the custom validators for email and username ensure that the values given are not duplicates rising an error if the mentioned
    # comes true.

    def validate_email(self,field):
        if field.data != self.user.email and \
                User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if field.data != self.user.username and \
                User.query.filter_by(username = field.data).first():
            raise ValidationError('Username already registered.')



class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?",validators=[Required()])
    submit =  SubmitField('Submit')
    