import os

import click
from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

from ticketing.database import init_db_command

__version__ = (0,1,0, "dev")

db = SQLAlchemy()

def init_app(test_config=None):
    """Construct the Core Application"""
    app = Flask(__name__, instance_relative_config=True)

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

    db.init_app(app)

    with app.app_context():
        from ticketing import database, auth, dashboard, customers, tickets

        # Database
        db.create_all() # Create the Sql tables for our existing models
        app.cli.add_command(init_db_command)

        #auth
        app.register_blueprint(auth.bp)

        #dashboard
        app.register_blueprint(dashboard.bp)
        app.add_url_rule('/', endpoint='index')
        
        #customers
        app.register_blueprint(customers.bp)

        #tickets
        app.register_blueprint(tickets.bp)

        return app

