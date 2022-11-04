from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    @classmethod
    def to_dict(cls, self):
        return {
            "id": self.goal_id,
            "title":self.title
        }