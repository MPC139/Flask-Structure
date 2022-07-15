from crypt import methods
from . import main
from flask import render_template, url_for, redirect


@main.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@main.route('/user/<name>',methods=['GET'])
def user(name):
    return render_template('user.html',name=name)