from app import db
from .task import Task


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def goal_from_dict(cls, response_dict):
        return cls(title=response_dict["title"]
        )

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }