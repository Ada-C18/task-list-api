from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }

    # @classmethod
    # def from_dict(cls, data_dict):
    #     # CHECK data_dict has all valid bike attributes
    #     if "title" in data_dict and "description" in data_dict and "completed_at" in data_dict:
    #         new_obj = cls(title=data_dict["title"],
    #                       description=data_dict["description"],
    #                       completed_at=data_dict["completed_at"],)
    #         return new_obj
