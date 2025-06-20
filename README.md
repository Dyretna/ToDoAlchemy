# Flaskr – Extended Version

This project is based on the official [Flask tutorial](https://flask.palletsprojects.com/en/latest/tutorial/), with extended testing and code structure improvements. The goal is to provide a clean, reliable starting point for future Flask-based applications.

## Features

- 100% test coverage with `pytest` and `coverage`
- Full authentication system (register, login, logout)
- Blueprint-based structure
- SQLite database integration with schema versioning
- HTML templates using Jinja2
- Easy to extend with new routes, models, or APIs

## Purpose

This repository serves as a minimal Flask project template with a complete testing setup. It's intended as a base for experimenting with new features or quickly spinning up production-ready prototypes.

## Technologies

- Python 3.x
- Flask
- Jinja2
- SQLite
- `pytest`
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

Running tests, generating visual coverage report (html)
```bash
coverage run -m pytest
coverage report -m
coverage html
```
