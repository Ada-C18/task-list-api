from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal")



    def to_dict(self):
        return {
            "id":self.goal_id,
            "title":self.title
        }
    
    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"]
        )