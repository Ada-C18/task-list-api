from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default = False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates = 'tasks' )
    
    
    def to_dict(self):
        task_dict = {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": False if self.completed_at is None else True
        }
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict

    
    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict  and "description" in data_dict and "is_complete" in data_dict:
            new_obj = cls(
            title=data_dict["title"], 
            description=data_dict["description"], 
            is_complete= data_dict["is_complete"])
            
            return new_obj


