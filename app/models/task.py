from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80)) 
    description  = db.Column(db.String(80)) 
    completed_at = db.Column(db.DateTime, unique = False, nullable = True)
    
    def build_task_dict(self):
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }
