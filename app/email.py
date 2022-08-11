import email
from . import mail
from flask_mail import Message
from flask import render_template, current_app
from threading import Thread

def send_async_email(app,msg):
    with app.app_context():
        # mail.connect()
        mail.send(msg)
        

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                     sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target= send_async_email, args=[app,msg])  # We use thread to implement asynchronous email
    thr.start()
    return thr
    
# Example of sending email
# send_email(current_app.config['FLASKY_ADMIN'], 'New User','mail/new_user', username=user.username)