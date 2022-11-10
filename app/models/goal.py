from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    task = db.relationship('Task', backref='Goal', lazy=True)


    def to_dict(self):
        goal_dict = {
            "id":self.id,
            "title":self.title
        }
        return goal_dict