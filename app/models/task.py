from app import db
from flask import make_response, abort


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)

    def to_json(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False

        if self.goal_id:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete,
                "goal_id": self.goal_id
            }
        else:
            return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": is_complete
            }
    
    def update(self,request_body):
        try:
            self.title = request_body["title"]
            self.description = request_body["description"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))
    
    @classmethod
    def create(cls, request_body):
        new_task = cls(
            title = request_body["title"],
            description = request_body["description"], 
        )
        return new_task


