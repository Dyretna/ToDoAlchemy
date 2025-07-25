import pytest
from flask import g, session
from flask_todo.models import User


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post("/auth/register", data={"username": "test", "password": "a"})
    print(response.status_code)
    print(response.data)
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        user = User.query.filter_by(username="test").first()
        assert user is not None


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("testuser", "testuser", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    response = auth.login(username="testuser", password="pw")
    print(response.status_code)
    print(response.data)
    assert response.headers["Location"] == "/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.username == "testuser"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("a", "test", b"Incorrect username"),
        ("testuser", "a", b"Incorrect password"),
    ),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
