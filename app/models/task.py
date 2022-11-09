from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)  
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return_dict = {
                    "id": self.task_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": bool(self.completed_at),
            }
        if self.goal_id:
            return_dict["goal_id"]= self.goal_id
        return return_dict

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=task_dict["completed_at"],
        )