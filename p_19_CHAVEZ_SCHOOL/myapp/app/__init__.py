#app init file 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
import logging
import os
from sqlalchemy import text
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv # bring in the load_dotenv function so that we

#from .question_routes import question_routes  # Import the function from your routes file




# load our environmental variables.

# Initialize extensions
migrate = Migrate()
login_manager = LoginManager()

from .database import db

def create_app(config_class=Config):
    app = Flask(__name__)
    load_dotenv('.env')

    app.config.from_object(config_class)
    login_manager.init_app(app)

    # Flask admin stuff

    db.init_app(app)
    migrate.init_app(app, db)

    # add the one view that we have so far. 

    # Initialize extensions with app


    #note that these are okay as its okay to talk about the namespace of a
    # package from within its init file


    from app.blueprints.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

#    from app.blueprints.ml_and_da import mlda_bp
#    app.register_blueprint(mlda_bp,url_prefix='/mlda')
#
#    from app.blueprints.student import student as student_bp
#    app.register_blueprint(student_bp, url_prefix='/student')
#
#    from app.blueprints.staff import staff as staff_bp
#    app.register_blueprint(staff_bp, url_prefix='/staff')
#
#    from app.blueprints.crud import crud as crud_bp
#    app.register_blueprint(crud_bp, url_prefix='/crud')



    #Adding routes that aren't attached to blueprints.

    @app.route('/')
    def index():
        return "Welcome to the main page of our application!"

#    add_question_routes(app)




    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/schoolapp.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('School app startup')

    return app




