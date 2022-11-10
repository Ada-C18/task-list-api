from app import db
from sqlalchemy.orm import relationship


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)
    
    
    def to_dict(self):
        goals_dict = {
            "id" : self.goal_id,
            "title" : self.title
        }
        
        return goals_dict

    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict:
            new_obj = cls(title=data_dict["name"])
            
            return new_obj
        