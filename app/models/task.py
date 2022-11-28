from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        completed = True if self.completed_at else False

        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": completed,
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
            
    @classmethod
    def from_dict(cls, task_data):

        return Task(title=task_data["title"], description=task_data["description"], completed_at=None)