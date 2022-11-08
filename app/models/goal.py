from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        goal = {
            "id" : self.goal_id,
            "title": self.title,
        }

        return goal 

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])