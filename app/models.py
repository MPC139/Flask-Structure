from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from . import login_manager

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS=0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User',backref = 'role', lazy = 'dynamic')

    def __repr__(self):
        return f'Role {self.name}'
    @staticmethod
    def insert_roles():
        roles = {
            'User':(Permission.FOLLOW |
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW |
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES|
                    Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role  = Role(name = r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

# The insert_roles() function does not directly create new role objects. Instead, it tries
# to find existing roles by name and update those. A new role object is created only for
# role names that aren’t in the database already. This is done so that the role list can be
# updated in the future when changes need to be made. To add a new role or change the
# permission assignments for a role, change the roles array and rerun the function. Note
# that the “Anonymous” role does not need to be represented in the database, as it is
# designed to represent users who are not in the database.
# To apply these roles to the database, a shell session can be used:
# (venv) $ flask shell
# >>> Role.insert_roles()
# >>> Role.query.all()
# [<Role u'Administrator'>, <Role u'User'>, <Role u'Moderator'>]

class User(UserMixin ,db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64),unique = True, index = True)
    username = db.Column(db.String(64),unique = True, index = True)
    password_hash = db.Column(db.String(128))
    favorite_color = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean,default = False)

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first() 

    # Token Verification
    def generate_confirmation_token(self,expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})
    
    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # Password logic
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

    # Role verification
    def can(self,permissions):
        """The can() method added to the User model performs a bitwise and operation between
            the requested permissions and the permissions of the assigned role. The method returns
            True if all the requested bits are present in the role, which means that the user should
            be allowed to perform the task. The check for administration permissions is so common
            that it is also implemented as a standalone is_administrator() method."""

        return self.role is not None and \
        (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
        


class AnonymousUser(AnonymousUserMixin):

    # Role verification
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))