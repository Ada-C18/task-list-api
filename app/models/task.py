from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_task_dict(self):
        if self.goal_id is not None:
            return {
                    "id": self.id,
                    "goal_id": self.goal_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.completed_at is not None
                }       

        else:
            return {
                    "id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.completed_at is not None
                } 

    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title = req_body['title'],
            description = req_body['description'],
            completed_at = req_body.get('completed_at', None)
        )
    
    