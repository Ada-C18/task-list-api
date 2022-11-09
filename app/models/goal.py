from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self, tasks=False):
        goal = {
            "id" : self.goal_id,
            "title": self.title
        }
        
        if tasks:
            goal["tasks"] = [task.to_dict() for task in self.tasks]

        return goal 

    def update(self, request_body):
        self.title = request_body["title"]

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])