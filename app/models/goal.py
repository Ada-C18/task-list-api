from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    tasks = db.relationship("Task", backref="goal", lazy=True)
    
    def to_json(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }