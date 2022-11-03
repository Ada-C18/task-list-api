from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None)

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["task_id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["completed_at"] = self.completed_at

        # return task_as_dict

    def update(self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]
        self.completed_at = request_body["completed_at"]

    @classmethod
    def from_dict(cls, task_data):
        return cls(title=task_data["title"], description=task_data["description"])