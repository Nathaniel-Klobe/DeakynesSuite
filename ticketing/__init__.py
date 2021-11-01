import os

from flask import Flask


def create_app(test_config=None):
    #create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'deakynes_ticketing.sqlite'),
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
    from . import db
    db.init_app(app)

    #auth blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    #dashboard blueprint
    from . import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')
    
    #customers blueprint
    from . import customers
    app.register_blueprint(customers.bp)

    #tickets blueprint
    from . import tickets
    app.register_blueprint(tickets.bp)

    #orders blueprint
    from . import orders
    app.register_blueprint(orders.bp)

    #rentals blueprint
    from . import rentals
    app.register_blueprint(rentals.bp)

    return app
