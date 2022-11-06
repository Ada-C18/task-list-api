from app import db
# import json

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # confirm null is default if task has not been completed
    completed_at = db.Column(db.DateTime, nullable=True)
    # is_complete = db.Column(db.Boolean)
# pretend code to push something up 

    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["is_complete"] = False
        # if self.completed_at == None:
        #     task_dict["is_complete"] = False

        # return json.dumps(task_dict)
        return task_dict
        # task_dict["completed_at"] = self.completed_at

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])

        return new_task
