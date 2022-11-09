from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True, default=None)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.task_id,
            # "goal_id": False if self.goal_id is None else True,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }

    def to_dict_with_goal_id(self):
        return {
            "id": self.task_id,
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }