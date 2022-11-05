from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    @classmethod
    def from_dict(cls, cls_dict):
        return cls(
            title = cls_dict["title"]
        )