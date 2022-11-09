from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_response_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        return goal_dict

    @classmethod
    def from_request_dict(cls, data_dict):
        new_obj = cls()
        new_obj.goal_id = None if "goal_id" not in data_dict else data_dict["goal_id"]
        new_obj.title = None if "title" not in data_dict else data_dict["title"]

        return new_obj

    

