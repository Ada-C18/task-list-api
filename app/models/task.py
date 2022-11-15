from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["is_complete"] = False
        task_as_dict["id"] = self.task_id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description

        return task_as_dict
    
    
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"],
            description = req_body["description"],
            completed_at = req_body["completed_at"]
        )
    


