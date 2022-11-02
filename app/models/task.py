from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
        }

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"], description=task_data["description"], completed_at=["completed_at"])
        return new_task
