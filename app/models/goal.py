from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal",lazy=True)
# Model Instance Methods
    def to_json(self):
        goal_dict = {
            "goal_id": self.goal_id,
            "title": self.title
        }
        return goal_dict
    @classmethod
    def from_json(cls, goal_data):
        if "title" in goal_data:
            new_goal = Goal(title=goal_data["title"])
            return new_goal