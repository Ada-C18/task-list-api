from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

def make_dict(self):
    """return a ditionary with all attributes of a goal"""
    goal_dict = {
        "id": self.goal_id,
        "title": self.title
    }

@classmethod
def from_dict(cls, data_dict):
    new_object = cls(
        title = data_dict["title"])
    return new_object
