from app import db
from sqlalchemy import sql
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }
        if self.goal_id:
            task["goal_id"] = self.goal_id
        return task

    def mark_complete(self, when=None):
        self.completed_at = (
            when
            if type(when) is datetime
            else (None if when is False else sql.func.now())
        )
