from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    @classmethod
    def from_dict(cls, task_data):
        return cls(title=task_data["title"],
                        description=task_data["description"])

    def to_dict(self):
        if self.goal_id:
            return dict(
            goal_id=self.goal_id,
            id=self.task_id, 
            title=self.title,
            description=self.description,
            is_complete=bool(self.completed_at)
        
        )
        else:
            return dict(
                id=self.task_id, 
                title=self.title,
                description=self.description,
                is_complete=bool(self.completed_at)
            
            )

