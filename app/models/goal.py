from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.TEXT)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        goal_dict = {"id": self.goal_id, "title": self.title
                     }
        return goal_dict

    @classmethod
    def from_dict(cls, data_goal):
        if data_goal["title"] == "":
            raise ValueError("goal must have a title")
        new_obj = cls(title=data_goal["title"])
        return new_obj
