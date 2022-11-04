from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        if not self.completed_at:
            task_dict["is_complete"] = False
        else:
            task_dict["completed_at"] = self.completed_at
        return task_dict

    @classmethod
    def from_dict(cls, input_dict):
        if "title" in input_dict and "description" in input_dict:
            new_task = cls(title=input_dict["title"], 
                description=input_dict["description"])
        if "completed_at" in input_dict:
            new_task.completed_at = input_dict["completed_at"]
        else:
            new_task.completed_at = None
        
        return new_task