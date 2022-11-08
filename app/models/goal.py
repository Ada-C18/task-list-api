from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    task_items = db.relationship("Task", back_populates="goal", lazy = True)

    def to_dict(self):
            goal_dict = {
                "id": self.goal_id,
                "title": self.title,
                # "task_items": [task.to_dict() for task in self.task_items]
            }
            return goal_dict

    # @classmethod
    # def from_dict(cls, obj_dict):
    #     new_obj = cls(
    #         goal_title = obj_dict["title"]
    #         )

    #     return new_obj