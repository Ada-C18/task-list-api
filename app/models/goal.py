from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        if self.tasks:
            return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": self.tasks
        }
        else:
            return {
                "id": self.goal_id,
                "title": self.title
            }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(
            title=goal_data["title"])
