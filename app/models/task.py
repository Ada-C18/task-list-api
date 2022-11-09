from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True) 
    
    def to_dict(self):
        if self.completed_at == None:
            return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }
        else:
            return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True
        }
        

    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict and "description" in data_dict:
            new_obj = cls(title=data_dict["title"], 
            description=data_dict["description"])
            
            return new_obj
# Wave 1 CRUD
# Tasks are entities that describe a task a user wants to complete. They contain a:
# title to name the task
# description to hold details about the task
# an optional datetime that the task is completed on
# Our goal for this wave is to be able to create, read, update, and delete 
# different tasks. We will create RESTful routes for this different operations.