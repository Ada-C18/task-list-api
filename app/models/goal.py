from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)


    def to_dict(self):
        goal_dict = {}
        goal_dict["id"] = self.id
        goal_dict["title"] = self.title
    
        return goal_dict