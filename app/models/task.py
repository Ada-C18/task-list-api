from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey(
        'goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
        if self.goal_id:
            task["goal_id"] = self.goal_id
        return task

    # @classmethod
    # def from_dict(cls, data_dict):
    #     # CHECK data_dict has all valid bike attributes
    #     if "title" in data_dict and "description" in data_dict and "completed_at" in data_dict:
    #         new_obj = cls(title=data_dict["title"],
    #                       description=data_dict["description"],
    #                       completed_at=data_dict["completed_at"],)
    #         return new_obj
