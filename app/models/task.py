from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    is_complete = db.Column(db.Boolean)
    completed_at = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }
        if not self.is_complete:
            task_dict["is_complete"] = False

        return task_dict

    @classmethod
    def from_dict(cls, input_dict):
        if "title" in input_dict and "description" in input_dict:
            new_task = cls(title=input_dict["title"], 
                description=input_dict["description"])
        if "is_complete" in input_dict:
            new_task.is_complete = input_dict["is_complete"]
        else:
            new_task.is_complete = False
        
        return new_task