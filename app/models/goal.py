from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal", lazy = True)

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title = goal_data["title"])
        return new_goal

    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] = self.goal_id
        goal_dict["title"] = self.title
        # goal_dict["tasks"] = self.tasks
        return goal_dict
