from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        result_dict = dict(
            # evaluates as False if null, True otherwise
            is_complete=bool(self.completed_at),
            title=self.title,
            id=self.id,
            description=self.description,
        )
        return result_dict

    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title=task_dict["title"],
            completed_at=task_dict["completed_at"],
            description=task_dict["description"],
        )
