from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    # tasks = db.relationship("Tasks", back_populates="goals")

    def to_dict(self):
        # tasks_list = [task.to_dict()for task in self.tasks]
        goal_dict = {
            "id": self.id,
            "title": self.title,
        }
        return goal_dict

    # @classmethod
    # def from_dict(cls, data_dict):
    #     # CHECK data_dict has all valid bike attributes
    #     if "title" in data_dict:
    #         new_obj = cls(title=data_dict["title"])
    #         return new_obj
