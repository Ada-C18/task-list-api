from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
            }

    def to_task_dict(self):
        return {
            "task": {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
            }       
        }     

    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title = req_body['title'],
            description = req_body['description'],
            completed_at = req_body.get('completed_at', None)
        )
    