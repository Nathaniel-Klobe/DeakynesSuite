import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from ticketing.database import init_db_command

__version__ = (0,1,0, "dev")

db = SQLAlchemy()

def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    db_url = 'postgres://localhost:5432/ticketing-test'

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        #Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py',silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #register database
    from ticketing import database
    db.init_app(app)
    app.cli.add_command(init_db_command)

    #auth blueprint
    from ticketing import auth
    app.register_blueprint(auth.bp)

    #dashboard blueprint
    from ticketing import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    
    #customers blueprint
    from ticketing import customers
    app.register_blueprint(customers.bp)

    #tickets blueprint
    from ticketing import tickets
    app.register_blueprint(tickets.bp)

    return app

