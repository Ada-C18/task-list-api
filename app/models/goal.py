from app import db
from flask import  abort, make_response



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal")


    @classmethod
    def from_dict(cls, task_data):
        new_goal = Goal(title=task_data["title"])
        return new_goal
    def to_dict(self):
        return dict(
            id = self.goal_id,
            title = self.title, 
            )
    
    

