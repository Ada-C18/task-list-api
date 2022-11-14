from app import db
from flask import current_app

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="task", lazy=True)

    def make_dict(self):
        new_dict = {
        "id": self.goal_id,
        "title": self.title,
        }
        return new_dict