from . import setting
from flask import render_template
from sqlalchemy.exc import IntegrityError, InvalidRequestError

@setting.app_errorhandler(404) # Fijarse que si usamos blueprint debemos poner setting.app_errorhandler(), cuando usamos directamente app queda app.errorhandler()
def page_not_found(e):
    return render_template('404.html') , 404


@setting.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html') , 500

@setting.app_errorhandler(IntegrityError)
def internal_database_error(e):
    return render_template('IntegrityError.html') , 700

