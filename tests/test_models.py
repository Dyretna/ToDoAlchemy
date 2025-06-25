import pytest
from flask_todo.models import db, User, Task


@pytest.fixture
def new_user():
    return User(username="testuser", password="hashedpassword")


@pytest.fixture
def new_task(new_user):
    return Task(
        user=new_user,
        title="Test Task",
        status="in progress",
        priority="high",
        description="A test task",
    )


def test_user_model_fields(new_user):
    assert new_user.username == "testuser"
    assert new_user.password == "hashedpassword"


def test_task_model_fields(new_task):
    assert new_task.title == "Test Task"
    assert new_task.status == "in progress"
    assert new_task.priority == "high"
    assert new_task.description == "A test task"
    assert new_task.user.username == "testuser"


def test_user_task_relationship(app):
    with app.app_context():
        user = User(username="reluser", password="pw")
        db.session.add(user)
        db.session.commit()
        task = Task(
            user_id=user.id,
            title="Rel Task",
            status="finished",
            priority="low",
            description="Relationship test",
        )
        db.session.add(task)
        db.session.commit()
        fetched_user = User.query.filter_by(username="reluser").first()
        assert len(fetched_user.tasks) == 1
        assert fetched_user.tasks[0].title == "Rel Task"
