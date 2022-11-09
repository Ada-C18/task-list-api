from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    is_complete=db.Column(db.Boolean, default=False)
    goal = db.relationship("Goal", back_populates="tasks")

    
    def to_dict(self):
        dict_task = dict(
            id = self.task_id,
            title = self.title, 
            description = self.description, 
            is_complete=False if self.completed_at is None else True
            )
        if self.goal_id:
            dict_task["goal_id"] = self.goal_id
        return dict_task
    @classmethod

    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"],
            description=response_dict["description"],
            # completed_at=None
        )