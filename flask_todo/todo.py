import datetime

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flask_todo.auth import login_required
from flask_todo.models import db, Task

bp = Blueprint("todo", __name__)


@bp.route("/")
def index():
    tasks = Task.query.order_by(Task.created.desc()).all()
    return render_template("todo/index.html", tasks=tasks)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        status = request.form["status"]
        priority = request.form["priority"]
        description = request.form["description"]
        due_str = request.form["due"]
        error = None

        due = None
        if due_str:
            try:
                due = datetime.datetime.strptime(due_str, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format for due date."

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            task = Task(
                user_id=g.user.id,
                title=title,
                status=status,
                priority=priority,
                description=description,
                due=due,
            )
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("todo.index"))

    return render_template("todo/create.html")


def get_task(id, check_author=True):
    task = Task.query.get_or_404(id)
    if check_author and task.user.id != g.user.id:
        abort(403)
    return task


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    task = get_task(id)

    if request.method == "POST":
        title = request.form["title"]
        status = request.form["status"]
        priority = request.form["priority"]
        description = request.form["description"]
        due_str = request.form["due"]
        error = None

        due = None
        if due_str:
            try:
                due = datetime.datetime.strptime(due_str, "%Y-%m-%d")
            except ValueError:
                error = "Invalid date format for due date."

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            task.user_id = g.user.id
            task.title = title
            task.status = status
            task.priority = priority
            task.description = description
            task.due = due
            db.session.commit()
            return redirect(url_for("todo.index"))

    return render_template("todo/update.html", task=task)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    task = get_task(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("todo.index"))
