from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def to_dict(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        task_dict = { "id": self.id,
        "title": self.title,
        "description": self.description,
        "is_complete": is_complete,
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    @classmethod
    def create_tasks(cls, task_data):
        return cls(title=task_data["title"], description=task_data["description"], completed_at=task_data["is_complete"])


