from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        goal_as_dict = {
        "id": self.goal_id,
        "title": self.title,
        }

        return goal_as_dict

    @classmethod
    def from_dict(cls, task_data):
        new_goal = cls(title=task_data["title"],
                        )

        return new_goal