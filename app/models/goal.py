from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] = self.goal_id
        goal_dict["title"] = self.title

        return goal_dict
