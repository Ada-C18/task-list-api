from app import db 
# from flask import abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at)
            # "goal_id": self.goal_id
        } 
        
    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title=req_body['title'],
            description=req_body['description']
        )
    
# def update(self, req_body):
#     try:
#         self.title = req_body["title"],
#         self.description = req_body["description"],
#         self.complete = req_body["completed_at"]
#     except KeyError as error:
#         abort(make_response({'message': f"Missing attribute: {error}"}))