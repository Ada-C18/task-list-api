from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), index = True, unique = False) 
    description  = db.Column(db.String(80), index = True, unique = False) 
    is_complete = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    
    def build_task_dict(self):
            return {
                "id": self.id,
                "title": self.name,
                "description": self.description,
                "is_complete": self.is_complete
            }