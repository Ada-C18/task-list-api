from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    tasks = db.relationship("Task", back_populates="goal")
    
    @classmethod
    def from_dict(cls, goal_data):
        new_task = Goal(title=goal_data["title"])
        return new_task
    
    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
            }