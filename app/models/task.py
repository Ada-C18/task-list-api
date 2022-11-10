from app import db
from app.models.goal import Goal
from flask import current_app

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)


    def create_dict(self):

        new_dict = {
        "id": self.task_id,
        "goal_id": self.goal_id,
        "title": self.title,
        "description": self.description,
        "is_complete": self.completed_at
        }

        if self.completed_at is None:
            new_dict["is_complete"] = False
        else:
            new_dict["is_complete"] = True

        if self.goal_id is None:
            new_dict.pop("goal_id")

        return new_dict
