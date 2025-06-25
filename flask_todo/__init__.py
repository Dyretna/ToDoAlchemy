import os

from flask import Flask
from .models import db
from . import auth, todo


def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "todo.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # load the instance config, if it exists, when not testing
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    # Load the test config if passed in
    else:
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # from imported modules (db, auth, todo)
    # initialize database and register blueprints.
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    app.add_url_rule("/", endpoint="index")

    return app
