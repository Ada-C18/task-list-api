from app import db
from app.models.task import Task

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title
        }

        if self.tasks:
            goal_dict["tasks"] = [task.to_dict() for task in self.tasks]

        return goal_dict

    def from_dict(goal_data):
        return Goal(
            title=goal_data["title"]
        )
