from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True )
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.task_id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["description"] = self.description

        return task_dict

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
        return new_task