from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy=True)

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["is_complete"] = False
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
            
        return task_as_dict
    
    
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at = req_body["completed_at"]
        )
    


