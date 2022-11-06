from app import db
import json


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean)


    def to_dict(self):
        task_as_dict = {"task": {}}
        # task_as_dict["id"] = self.id
        task_as_dict["task"]["title"] = self.title
        task_as_dict["task"]["description"] = self.description
        task_as_dict["task"]["is_complete"] = self.is_complete
        

        return json.dumps(task_as_dict)