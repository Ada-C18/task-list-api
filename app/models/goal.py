from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    task = db.relationship("Task", back_populates="goal")

    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }

    