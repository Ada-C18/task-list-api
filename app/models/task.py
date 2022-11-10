from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.check_if_complete()
        }

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=None)

    def check_if_complete(self):
        if self.completed_at:
            return True
        else:
            return False

    def mark_complete(self):
        self.completed_at = datetime.now()

    def mark_incomplete(self):
        self.completed_at = None