from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    # add relation to tasks
    tasks = db.relationship("Tasks", back_populates="goal", lazy="True")
    # "lazy" - how the data for relationship is loaded

    def to_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title}

        return goal_dict
