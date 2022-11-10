from app import db
from flask import current_app

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json_goal(self):
        return{
            "goal_id": self.goal_id,
            "title": self.title
        }