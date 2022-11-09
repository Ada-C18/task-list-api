from app import db
from datetime import datetime
from flask import abort, make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    description=db.Column(db.String)
    completed_at=db.Column(db.DateTime)
    is_complete=db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    def to_dict(self):
        if self.goal_id:
            
        
            return dict(
                id= self.id,
                goal_id=self.goal_id,
                title=self.title,
                description= self.description,
                is_complete=False
            
            )
            
        return dict(
                id= self.id,
                title=self.title,
                description= self.description,
                is_complete=False
            
        )

    def from_dict(self):
        
        return dict(
            id= self.id,
            title= self.title,
            description= self.description,
            is_complete=True
            
    )   

