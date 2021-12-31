import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import app

engine = create_engine('')
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import ticketing.models
    Base.metadata.create_all(bind=engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
