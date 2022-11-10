from app import db
import sqlalchemy as sa
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False) 
    description = db.Column(db.String, nullable=False) 
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    def from_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }