from app import db
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates='goal', lazy=True)

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title

        if self.tasks:
            goal_as_dict["tasks"] = self.tasks.title 

        return goal_as_dict
    
    
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"]
        )
