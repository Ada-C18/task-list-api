from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80)) 
    task_rel = db.relationship("Task", backref="goal",lazy=True) 

    def goal_dict(self):
            return {
                "id": self.goal_id,
                "title": self.title}
    
    @classmethod
    def from_dict(cls, goal_data):
        new_Goal = Goal(title=goal_data["title"])
        return new_Goal