# ToDoAlchemy

This project is based on the official [Flask tutorial](https://flask.palletsprojects.com/en/latest/tutorial/), but has been refactored to use SQLAlchemy and reworked into a simple ToDo application. The authentication system and blueprint structure remain, but all database access is now handled via SQLAlchemy models. The tests have not yet been refactored for SQLAlchemy—this will be addressed in a future version.

## Features

- ToDo list management (create, view, update, delete tasks)
- Full authentication system (register, login, logout)
- Modular blueprint-based structure
- Database integration via SQLAlchemy ORM
- HTML templates using Jinja2
- Easy to extend with new routes, models, or APIs

## Purpose

This repository serves as a modern Flask project template with SQLAlchemy and a basic ToDo app as an example. It's intended as a starting point for your own projects or prototypes.

## Technologies

- Python 3.x
- Flask
- SQLAlchemy
- Jinja2
- SQLite
- `pytest` (tests not yet refactored for SQLAlchemy)
- `coverage`

## Getting Started

Install the project in editable mode:
```bash
pip install -e .
```

Initialize the database:
```bash
flask --app flaskr init-db
```

Run the development server:
```bash
flask --app flaskr run
```

## Testing & Coverage

The tests are not yet updated for SQLAlchemy. This will be improved in a future release.

To run tests and generate a coverage report (HTML):
```bash
coverage run -m pytest
coverage report -m
coverage html
```

## Code Style & Tooling

This project uses [pre-commit](https://pre-commit.com/) hooks to ensure consistent code style and automatic formatting before each commit.

To enable:
```bash
pip install pre-commit
pre-commit install
```
To manually run on all files:
```bash
pre-commit run --all-files
```

The following checks are configured in `.pre-commit-config.yaml`:
- black: code formatting
- ruff: linting & autofix
- end-of-line-fixer: final newline enforcement
