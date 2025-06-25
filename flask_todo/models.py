from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(20), default="not started", nullable=False)
    priority = db.Column(db.String(20), default="middle", nullable=False)
    description = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, server_default=db.func.now())
    due = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref="tasks", lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
