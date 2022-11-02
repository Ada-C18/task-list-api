## Code Coverage code:

pytest --cov=app --cov-report html --cov-report term

SQLALCHEMY_DATABASE_URI = postgresql+psycopg2://postgres:postgres@localhost:5432/tasklist_dev
SQLALCHEMY_TEST_DATABASE_URI = ostgresql+psycopg2://postgres:postgres@localhost:5432/tasklist_test

from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTIme, default=None, nullable=True)


