from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable = False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"], description=data_dict["description"])

    def to_dict(self):
        completed = None
        if not self.completed_at:
            completed = False
        else:
            completed = True 
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": completed
            }

    # def to_dict_one(self):
    #     completed = None
    #     if not self.completed_at:
    #         completed = False
    #     else:
    #         completed = True 
    #     return {
    #         "task": {
    #             "id": self.task_id,
    #             "title": self.title,
    #             "description": self.description,
    #             "is_complete": completed }
    #         }