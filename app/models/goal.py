from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    @classmethod
    def from_goal_dict(cls, goal_data):
        return cls(goal_title=goal_data["title"])



    def to_dict_goal(self):
        return dict(
            id=self.goal_id, 
            title=self.goal_title
        
        )