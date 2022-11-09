from app import db
from flask import abort, make_response

#Child
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at) 
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )

def update(self, req_body):
        try: 
            self.title = req_body["title"]
            self.description = req_body["description"]
            self.completed_at = None
            

        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))