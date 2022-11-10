from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable = False)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])

    def to_dict(self):
        return dict(
            id=self.goal_id,
            title=self.title
        )