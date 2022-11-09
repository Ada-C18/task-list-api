from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) # todo: nullable default=None?
    is_complete = db.Column(db.Boolean, default=False) # False until wave 3

    def to_dict(self):
        if self.completed_at is not None: 
            return {
                "id":self.task_id,
                "title":self.title,
                "description":self.description,
            #    "completed_at": self.completed_at,
                "is_complete": self.is_complete
            }
        else:
            return {
                "id":self.task_id,
                "title":self.title,
                "description":self.description,
                "is_complete": self.is_complete
            }

    @classmethod
    def from_dict(cls, task_dict):
        if not "is_complete" in task_dict:
            task_dict["is_complete"] = False
        
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            is_complete=task_dict["is_complete"]
        )