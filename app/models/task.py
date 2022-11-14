from app import db
from flask import current_app,request
from sqlalchemy import desc,asc
from dotenv import load_dotenv


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)

    def task_dict(self):
        task_dict = {"id": self.task_id, "title": self.title, "description": self.description, "is_complete": False if self.completed_at != None else True}

        return task_dict


