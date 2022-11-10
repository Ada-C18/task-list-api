from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_json(self):
        task_as_json = {}
        task_as_json["id"] = self.task_id
        task_as_json["title"] = self.title
        task_as_json["description"] = self.description
        task_as_json["is_complete"] = False
        return task_as_json
    
    @classmethod
    def from_json(cls, task_data):
        new_task = cls(
            title=task_data["title"],
            description=task_data["description"],
        )
        return new_task

