import pytest
from flask_todo.models import db, User, Task
from werkzeug.security import generate_password_hash
from datetime import date


def test_index(client, auth, app):
    response = client.get("/")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    with app.app_context():
        # Create a test-user and a task
        user = User.query.filter_by(username="testuser").first()
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            title="test title",
            status="pending",
            priority="high",
            due=date.today(),
            description="test\ndescription",
        )
        db.session.add(task)
        db.session.commit()

    auth.login(username="testuser", password="pw")
    response = client.get("/")
    assert b"Log Out" in response.data
    assert b"test title" in response.data
    assert b"Created by: testuser" in response.data
    assert b"test\ndescription" in response.data
    assert b'href="/1/update"' in response.data
    assert bytes(str(date.today()), "utf-8") in response.data


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
        "/1/delete",
    ),
)
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        user1 = User(username="user1", password=generate_password_hash("pw"))
        user2 = User(username="user2", password=generate_password_hash("pw"))
        db.session.add_all([user1, user2])
        db.session.commit()
        task = Task(
            user_id=user2.id,
            title="Other's task",
            status="pending",
            priority="low",
            description="desc",
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    auth.login(username="user1", password="pw")
    assert (
        client.post(
            f"/{task_id}/update",
            data={
                "title": "created",
                "status": "pending",
                "priority": "low",
                "description": "desc",
            },
        ).status_code
        == 403
    )
    assert client.post(f"/{task_id}/delete").status_code == 403


@pytest.mark.parametrize(
    "path",
    (
        "/2/update",
        "/2/delete",
    ),
)
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login(username="testuser", password="pw")
    get_resp = client.get("/create")
    print("GET /create status:", get_resp.status_code)
    post_resp = client.post(
        "/create",
        data={
            "title": "created",
            "status": "pending",
            "priority": "low",
            "due": date.today().strftime("%Y-%m-%d"),
            "description": "desc",
        },
    )
    print("POST /create status:", post_resp.status_code)
    print("POST /create data:", post_resp.data)

    with app.app_context():
        task = Task.query.filter_by(title="created").first()
        assert task is not None
        assert task.title == "created"
        assert task.user is not None
        assert task.user.username == "testuser"


def test_update(client, auth, app):
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            title="old title",
            status="not started",
            priority="low",
            description="old desc",
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    auth.login(username="testuser", password="pw")
    assert client.get(f"/{task_id}/update").status_code == 200
    client.post(
        f"/{task_id}/update",
        data={
            "title": "updated",
            "status": "pending",
            "priority": "middle",
            "due": date.today().strftime("%Y-%m-%d"),
            "description": "desc",
        },
    )

    with app.app_context():
        task = Task.query.get(task_id)
        assert task is not None
        assert task.title == "updated"
        assert task.user is not None
        assert task.user.username == "testuser"


@pytest.mark.parametrize(
    "path",
    (
        "/create",
        "/1/update",
    ),
)
def test_create_update_validate(client, auth, app, path):
    if path == "/1/update":
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            db.session.add(user)
            db.session.commit()
            task = Task(
                user_id=user.id,
                title="old title",
                status="not started",
                priority="low",
                description="old desc",
            )
            db.session.add(task)
            db.session.commit()
    auth.login(username="testuser", password="pw")
    response = client.post(
        path,
        data={
            "title": "",
            "status": "pending",
            "priority": "low",
            "due": date.today().strftime("%Y-%m-%d"),
            "description": "",
        },
    )
    assert b"Title is required." in response.data


def test_delete(client, auth, app):
    with app.app_context():
        user = User.query.filter_by(username="testuser").first()
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            title="to be deleted",
            status="pending",
            priority="low",
            due=date.today(),
            description="desc",
        )
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    auth.login(username="testuser", password="pw")
    response = client.post(f"/{task_id}/delete")
    assert response.headers["Location"] == "/"

    with app.app_context():
        task = Task.query.get(task_id)
        assert task is None
