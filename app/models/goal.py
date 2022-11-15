from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"] = self.goal_id
        goal_as_dict["title"] = self.title

        return goal_as_dict
    
    
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"]
        )
