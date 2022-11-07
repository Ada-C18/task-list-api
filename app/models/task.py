from app import db
from datetime import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        task = {
            "id" : self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }

        return task

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]

    def mark_complete(self, completion_time=None):
        if completion_time is not False:
            self.completed_at = datetime.utcnow()
        else:
            self.completed_at = None

    @classmethod
    def from_dict(cls, task_data):
        return cls(title=task_data["title"], description=task_data["description"])