from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def to_response_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }

        if self.goal_id is not None:
            task_dict["goal_id"] = self.goal_id
            
        return task_dict

    @classmethod
    def from_request_dict(cls, data_dict):
        new_obj = cls()
        new_obj.task_id = None if "id" not in data_dict else data_dict["id"]
        new_obj.title = None if "title" not in data_dict else data_dict["title"]
        new_obj.description= None if "description" not in data_dict else data_dict["description"]
        new_obj.completed_at= None if "completed_at" not in data_dict else data_dict["completed_at"]
        
        return new_obj

    def is_complete(self):
        return False if self.completed_at == None else True



