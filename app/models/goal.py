from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    # Lazy parameter determines how the related objects get loaded
    # when querying through relationships.


    def return_body(self):
        return {
            "id": self.goal_id,
            "title": self.title
        }
    

    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict:
            new_obj = cls(title=data_dict["title"])
            return new_obj
    

