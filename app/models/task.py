from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"], description=data_dict["description"])

    def to_dict(self):
        if self.goal_id:
            return {
                    "id": self.task_id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.check_complete()
                }
                
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.check_complete()
        }

    def check_complete(self):
        if self.completed_at:
            return True
        else:
            return False