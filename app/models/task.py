from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=True, default=False)

    @classmethod
    def task_from_dict(cls, response_dict):
        return cls(title=response_dict["title"],
        description=response_dict["description"], 
        is_complete=response_dict.get("is_complete", False)
        )

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }