from app import db
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete= bool(self.completed_at)
        )
            
    @classmethod
    def from_dict(cls, task_data):
        # new_task = 
        return Task(title=task_data["title"], description=task_data["description"], completed_at=None)# changed from completed_at NONE
        # return Task(title=task_data["title"], description=task_data["description"], is_complete=None)# changed from completed_at

    def to_goal_dict(self):
        return {
            "id": self.id,
            "goal_id": self.goal_id,
        }