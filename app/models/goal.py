from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_json(self):
        goal_as_json = {}
        goal_as_json["id"] = self.goal_id
        goal_as_json["title"] = self.title
        return goal_as_json
    
    @classmethod
    def from_json(cls, goal_data):
        new_goal = cls(
            title=goal_data["title"]
        )
        return new_goal
