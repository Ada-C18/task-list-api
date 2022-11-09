from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        if self.goal_id is not None:
            task_dict = {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True if self.completed_at else False,
                }
        else:
            task_dict = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": True if self.completed_at else False,
                }
        return task_dict

    @classmethod
    def from_dict(cls, obj_dict):
        new_obj = cls(
            title = obj_dict.get("title", None),
            description = obj_dict.get("description", None),
            completed_at = obj_dict.get("completed_at", None),
            # goal_id = obj_dict["goal_id"]
            )

        return new_obj