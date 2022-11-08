from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"],
            description=response_dict["description"],
            completed_at=None
        )
    
    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete()
        )

    def to_dict_with_goal_id(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=self.is_complete(),
            goal_id=self.goal_id
        )


    def is_complete(self):
        if self.completed_at:
            return True
        else:
            return False

   
