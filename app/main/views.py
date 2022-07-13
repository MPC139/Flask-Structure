from . import main

@main.route('/')
def index():
    return '<h1>Hello world2!</h1>'

@main.route('/user/<name>')
def user(name):
    return f'<h1>Hello {name}</h1>'