from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80)) 
    description  = db.Column(db.String(80)) 
    completed_at = db.Column(db.DateTime, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)

    def build_task_dict(self):
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)
            }

    @classmethod
    def from_dict(cls, task_data):
        new_Task = cls(title=task_data["title"],
                        description=task_data["description"],
                        is_complete=task_data["completed_at"],
                        completed_at=task_data.get("is_complete", None),)
        return new_Task