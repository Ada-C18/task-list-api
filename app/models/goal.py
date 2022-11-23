from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", backref='goal', lazy=True)

    def to_dict(self):
        if self.tasks:
            return dict(
                id = self.goal_id,
                title = self.title,
                tasks=[task.to_dict() for task in self.tasks])

        else:
            return dict(
            id = self.goal_id,
            title = self.title)
    

    @classmethod
    def from_dict(cls, data_dict):
            return Goal(title = data_dict["title"])
                    


