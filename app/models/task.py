from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        task_dict = {"id": self.task_id, "title": self.title,
                     "description": self.description,
                     "is_compelet": self.completed_at is not None
                     }
        return task_dict

    @classmethod
    def from_dict(cls, data_dic):
        new_obj = cls(title=data_dic["title"],
                      description=data_dic["description"],
                      completed_at = data_dic.get("completed_at"))

        return new_obj
