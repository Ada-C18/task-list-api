from app import db
from sqlalchemy import ForeignKey

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, ForeignKey('goal.goal_id'))

    def to_dict(self):
        task_dict = {
            
                "id" : self.task_id,
                "title": self.title,
                "description" : self.description,
                "is_complete" : True if self.completed_at else False
            } 
        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id

        return task_dict
        
    
    @classmethod
    def from_dict(cls,data_dict):
        
        if "title" in data_dict and "description" in data_dict and "is_complete" in data_dict:
            new_obj = cls(title = data_dict["title"],
                    description = data_dict["description"],
                    is_complete = data_dict["is complete"]
                    )
            return new_obj
        
        