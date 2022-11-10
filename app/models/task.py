from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def to_dict(self):
        task_dict = {}
        if self.goal_id is not None:
            task_dict = {
                "id": self.task_id,
                "goal_id": self.goal_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            } 
        else:
            task_dict = {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.is_complete
            }
        return task_dict
    
    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict and "description" in data_dict:
            new_obj = Task(title=data_dict["title"], description=data_dict["description"])
            return new_obj