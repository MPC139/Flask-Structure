from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment

bootstrap = Bootstrap()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)

    bootstrap.init_app(app)
    moment.init_app(app)

    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app