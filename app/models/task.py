from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    def to_dict(self):
        task_dict = {}
        task_dict["id"] = self.task_id
        task_dict["title"] = self.title
        task_dict["description"] = self.description
        task_dict["completed_at"] = self.completed_at

        return task_dict

    @classmethod
    def from_dict(cls, req_body):
        return cls(title=req_body["title"],
            description=req_body["description"],
            completed_at=req_body["completed_at"])