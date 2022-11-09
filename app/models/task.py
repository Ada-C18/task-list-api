from app import db
from flask import abort, make_response

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    
    def to_json(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False,
            "goal_id": self.goal_id if self.goal_id else None
        }
        
    @classmethod
    def from_dict(cls, req_body):
        return cls(
        title=req_body["title"],
        description=req_body["description"],
        completed_at=req_body.get("completed_at")
        )

    def update(self, req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
            self.completed_at = req_body.get("completed_at")
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))