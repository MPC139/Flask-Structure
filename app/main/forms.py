from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,TextAreaField
from wtforms.validators import Required,Length


class EditProfileForm(FlaskForm):
    name = StringField('Real name', validators=[Length(1,64)])
    location = StringField('Location', validators=[Length(1,64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

