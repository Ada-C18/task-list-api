from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=True, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def task_from_dict(cls, response_dict):
        return cls(title=response_dict["title"],
        description=response_dict["description"], 
        completed_at=response_dict.get("completed_at", None),
        is_complete=response_dict.get("is_complete", False)
        )

    def to_dict(self):
        if self.goal_id:
            return {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }