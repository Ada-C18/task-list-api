from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False)

    @classmethod
    def from_dict(cls,data_dict):
        return cls(
            title=data_dict["title"]
            )

    def to_dict(self):
        return dict(
            id=self.id,
            title=self.title
        )