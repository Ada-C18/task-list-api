from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def make_dict(self):
        """return a ditionary with all attributes of a goal"""
        goal_dict = {
            "id": self.id,
            "title": self.title
        }
        return goal_dict

    @classmethod
    def from_dict(cls, data_dict):
        new_object = cls(
            title = data_dict["title"])
        return new_object
