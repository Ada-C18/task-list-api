from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Many tasks to one goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        result_dict = {}
        result_dict["id"] = self.task_id
        result_dict["title"] = self.title
        result_dict["description"] = self.description
        result_dict["completed_at"] = self.completed_at

        return result_dict

    @classmethod
    def from_dict(cls, req_body):
        return cls(title=req_body["title"],
            description=req_body["description"],
            completed_at=req_body["completed_at"])