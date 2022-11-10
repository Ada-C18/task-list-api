from app import db
from datetime import date



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)
    goal = db.relationship("Goal", back_populates='tasks')

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = bool(self.is_complete)

        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id

        return task_as_dict
    
    @classmethod
    def from_dict(cls, request_body):
        return cls(
            id=request_body["id"],
            title=request_body["title"],
            description=request_body["description"],
            goal_id=request_body["goal_id"],
            is_complete=request_body["is_complete"])

    def mark_complete(self):
        today = date.today()
        self.completed_at = today
        if self.completed_at:
            self.is_complete = True

    def mark_incomplete(self):
        self.completed_at = None
        self.is_complete = False