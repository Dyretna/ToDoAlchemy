from flask_todo import create_app
from flask_todo.models import db

app = create_app()
with app.app_context():
    db.create_all()
    print("Database initialized!")
