import email
from . import db
from werkzeug.security import generate_password_hash,check_password_hash


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User',backref = 'role')

    def __repr__(self):
        return f'Role {self.name}'

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),unique = True, index = True)
    password_hash = db.Column(db.String(128))
    favorite_color = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"User {self.username}"