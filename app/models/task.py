from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False) 
    description = db.Column(db.String, nullable=False) 
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    def from_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }
    
    def goals_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "goal_id" : self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete
        }