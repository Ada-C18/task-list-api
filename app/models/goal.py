from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # tasks = db.relationship("Task", back_populateds="goal")
    # "goal" here is related to goal = db.relationship("Goal", back_populated="tasks")


    def return_body(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }