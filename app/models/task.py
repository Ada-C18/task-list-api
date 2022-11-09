from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), default=None, nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
        if self.goal:
            task_dict["goal_id"] = self.goal.goal_id
            # task_dict["goal"] = self.goal.title

        return task_dict

    def from_dict(task_data):
        return Task(
            title=task_data["title"],
            description=task_data["description"],
            goal=task_data["goal"]
        )

