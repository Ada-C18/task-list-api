from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String,)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True )#default = None 
    # is_complete = db.Column(db.Boolean, default = False)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False                                  
        }
        
        # return {"task":{
        # "id": self.task_id,
        # "title": self.title,
        # "description": self.description,
        # "is_complete": True if self.completed_at else False}                               
        # }
        
    #note for improvement: we can create another function that call to_dict as value and task as key.