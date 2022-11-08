from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # add relation to tasks
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    # "lazy" - how the data for relationship is loaded

    def to_dict(self):
        # tasks_list = [task.to_dict() for task in self.tasks]

        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
            # "tasks": tasks_list
        }

        # if self.tasks:
        #     goal_dict["tasks"] = self.tasks

        return goal_dict
