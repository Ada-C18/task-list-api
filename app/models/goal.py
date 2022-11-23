from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def to_goal_dict(self):
        return dict(
            id = self.id,
            title = self.title
        )
    
    @classmethod
    def from_goal_dict(cls, data_dict):
        return Goal(title = data_dict["title"])    