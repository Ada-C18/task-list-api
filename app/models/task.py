from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)

    # adding FK for parent Goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    # define database relation with back_populates
    goal = db.relationship("Goal", back_populates="tasks")
    # Recommendation: Setting the nullable to True
    # nullable=True

    # converts Task object into Dict
    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
        }

        # is_complete is a "derived value"
        # if self.completed_at is None:
        #     task_dict["is_complete"] = False
        # else:
        #     task_dict["is_complete"] = True

        return task_dict
