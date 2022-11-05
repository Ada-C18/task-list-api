from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)



    def to_dict(self):
        return dict(
            id=self.task_id,
            title=self.title,
            description=self.description,
            is_complete=False
        )
    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"],
            description=response_dict["description"],
            completed_at=None
        )