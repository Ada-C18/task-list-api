from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.string)
    description = db.Column(db.string)
    completed_at = db.Column(db.datetime, nullable=True, default=datetime.utcnow)