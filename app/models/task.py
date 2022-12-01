from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")




    def to_dict(self):

        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False,
           # "completed_at": self.completed_at
            
        }
        
        if self.goal_id:
            task_dict["goal_id"] = self.goal_id
        
        return task_dict
    
    @classmethod   
    def from_dict(cls, req_body):
        return cls(
            title= req_body["title"] if "title" in req_body else None,
            description= req_body["description"] if "description" in req_body else None,
            completed_at= None 
        )
    
    def is_valid(self):
        if self == None:
            return False
        if self.title == None or self.title == "":
            return False
        if self.description == None or self.description == "":
            return False
        return True