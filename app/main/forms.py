from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import Required



class NameForm(FlaskForm):
    user = StringField('Username: ', validators=[Required()])
    password = PasswordField('Password:',validators=[Required()])
    favorite_color = StringField('Favorite Color: ')
    submit = SubmitField('Submit')

