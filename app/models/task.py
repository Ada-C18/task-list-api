from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80)) 
    description  = db.Column(db.String(80)) 
    completed_at = db.Column(db.DateTime, unique = False, nullable = True)
    goal_rel = db.relationship("Goal", back_populates="goal",lazy='True')
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id')) 

    def build_task_dict(self):
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }

    @classmethod
    def from_dict(cls, book_data):
        new_Task = Task(title=book_data["title"],
                        description=book_data["description"],
                        is_complete=bool["completed_at"])
        return new_Task