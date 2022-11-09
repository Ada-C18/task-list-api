from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task",back_populates="goal",lazy=True)
    


    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] = self.id
        goal_dict["title"] = self.title
        if self.tasks:
            goal_dict["goal_id"]= self.goal_id
        return goal_dict