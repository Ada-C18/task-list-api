from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)


    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
        return task_dict

    @classmethod
    def from_dict(cls, obj_dict):
        new_obj = cls(
            title = obj_dict.get("title", None),
            description = obj_dict.get("description", None),
            completed_at = obj_dict.get("completed_at", None)
            )

        return new_obj