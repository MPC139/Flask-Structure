import unittest
import socket
from flask import current_app
from app import create_app,db, email,mail
import app
from app.models import Role,User
from sqlalchemy.exc import IntegrityError



class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        mail.init_app(self.app)
        self.db = db
        self.db.init_app(self.app)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.mail = mail



    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertTrue(self.app is not None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_commit_db_unique_twice(self):
        role_test = Role(name = 'test')
        user_test = User(username = 'testing',password = '1234',favorite_color = 'red', role = role_test,email = 'test@test.com',confirmed =True)
        user_test2 = User(username = 'testing',password = '1234',favorite_color = 'red', role = role_test,email = 'test@test.com',confirmed =True)
        self.db.session.add_all([role_test,user_test,user_test2])
        with self.assertRaises(IntegrityError):
            self.db.session.commit()

    def test_commit_db(self):
        role_test_ = Role(name = 'test')
        user_test_ = User(username = 'testing',password = '1234',favorite_color = 'red', role = role_test_,email = 'test@test.com',confirmed =True)
        self.db.session.add_all([role_test_,user_test_])
        self.assertTrue(self.db.session.commit() is None)
        Role.query.filter_by(name = 'test').delete()
        User.query.filter_by(username = 'testing').delete()
        self.db.session.commit()

    def test_server_mail_is_up(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((self.app.config['MAIL_SERVER'], self.app.config['MAIL_PORT']))
        self.assertEqual(result,0)

