from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable= True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        result = dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = bool(self.completed_at)
        )

        if self.goal_id:
            result["goal_id"] = self.goal_id
            
        return result

    @classmethod
    def from_dict(cls, task_data):
        new_task = cls(title=task_data["title"],
                    description=task_data["description"])
        if "completed_at" in task_data:
            new_task.completed_at=task_data["completed_at"]
                        
        return new_task
        




            