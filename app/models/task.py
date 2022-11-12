from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
        }

        if self.completed_at == None:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True

        return task_dict

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title = task_dict["title"],
            description = task_dict["description"]
        )

