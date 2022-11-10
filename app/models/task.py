from app import db
from flask import abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal",back_populates="tasks")

    def to_dict(self):
        return {
                "id":self.task_id,
                "title": self.title,
                "description":self.description, 
                "is_complete":bool(self.completed_at)
                }

    @classmethod
    def from_dict(cls, task_data):
        try:
            new_task = Task(title=task_data["title"],
                            description=task_data["description"])
        except KeyError as error: 
            abort(make_response({"details":"Invalid data"},400))
        return new_task
    
    def update(self, req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"},400))





    

    
    
