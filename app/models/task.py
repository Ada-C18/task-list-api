from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String,)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True )#default = None 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        # return {
        #     "id": self.task_id,
        #     "title": self.title,
        #     "description": self.description,
        #     "is_complete": True if self.completed_at else False                                              
        # }
        dict = {        
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False                                              
        }
        
        if self.goal_id:
            dict["goal_id"] = self.goal_id
        return dict
            
    def to_dict_goal_id(self):
        dict = self.to_dict()
        dict["goal_id"] = self.goal_id
        return dict
            
    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            # goal_id=task_dict["goal_id"]                        
        )
    
    @classmethod
    def from_dict_goal_id(cls, task_dict):
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            goal_id=task_dict["goal_id"]                        
        )
    