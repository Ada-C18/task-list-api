from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }
    
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            is_complete=False
        )

