import datetime
from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates = "tasks")

    @classmethod
    def from_json(cls, req_body):
        return cls(
            title = req_body["title"],
            description = req_body["description"]
            ) 

    def to_dict(self):
        ret = {
                "task": {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
                }}
        if self.goal_id:
            ret["task"]["goal_id"] = self.goal_id
        return ret
    
    def update(self, req_body):
        try:
            self.title = req_body["title"],
            self.description = req_body["description"]
        except KeyError as error:
            raise error
        
        