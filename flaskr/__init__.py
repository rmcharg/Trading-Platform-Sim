from flask import Flask, session
from flask_session import Session
from os import path
import sqlite3


DATABASE_NAME = 'flaskr/trade.db'
CREATE_TABLES = "flaskr/schema.sql"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'uhfoauwheoachowehico'

    # Configure sessions to use filesystem 
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_COOKIE_PATH"] = "/"
    Session(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database()
    
    return app

def create_database():
    # If database does not exist create it with schema from file
    # if it does exist the connect to it.
    if not path.exists(DATABASE_NAME):
        print('Database does not exist! Creating database.')
        db = sqlite3.connect(DATABASE_NAME).cursor()
        
        with open(CREATE_TABLES) as f:
            sql_script = f.read()
        
        print('Initialising database tables!')
        db.executescript(sql_script)
    else:
        print('Database exists, connecting!')
        db = sqlite3.connect(DATABASE_NAME).cursor()

    return db