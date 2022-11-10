from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"])

    def to_dict(self, tasks=False):
        if not self.tasks and tasks == False:
            return {
            "id": self.goal_id,
            "title": self.title 
            }
        else:
            return {
                "id": self.goal_id,
                "title": self.title,
                "tasks": [task.to_dict(goal=True) for task in self.tasks]
                }
