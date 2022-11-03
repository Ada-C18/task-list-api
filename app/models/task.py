from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True, default=None)
    goal = db.relationship("Goal", back_populates='tasks')

    def dictionfy(self):
        return_dict={
            "id":self.task_id,
            "title":self.title,
            "description":self.description,
            "is_complete": True if self.completed_at is not None else False
        }
        if self.goal_id is not None:
            return_dict["goal_id"]=self.goal_id
        return return_dict