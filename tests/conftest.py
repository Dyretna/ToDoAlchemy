import os
import tempfile

import pytest
from flask_todo import create_app
from flask_todo.models import db, User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )

    with app.app_context():
        db.create_all()
        user = User(username="testuser", password=generate_password_hash("pw"))
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.engine.dispose()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="testuser", password="pw"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
