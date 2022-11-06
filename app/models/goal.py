from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"]
        )

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
        )
