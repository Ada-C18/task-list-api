from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.String, nullable=True, default=None)

    @classmethod
    def from_dict(cls,data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
            )

    def to_dict(self):
        if not self.completed_at:
            self.completed_at = False
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at
        )
