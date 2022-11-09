from app import db
from sqlalchemy.orm import relationship
from flask import make_response, abort
from datetime import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable = True)
    goal = relationship("Goal", back_populates="tasks")

    def to_dict(self):
        is_complete = False if self.completed_at == None else True
        if self.goal_id:
            return{
                   "goal_id": self.goal_id,
                   "id": self.task_id,
                   "title": self.title,
                   "description": self.description,
                   "is_complete": is_complete,
                   }
        else:
            return {
                    "id": self.task_id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": is_complete,
                   }
    @classmethod
    def from_dict(cls, data):
        if "datetime" not in data or "datetime" == None:
            data["datetime"] = None
        else:
            try:
                data["datetime"] = datetime.strptime(data["datetime"], '%m/%d/%y')
            except:
                abort(make_response({"details":f"datetime invalid, needs to be in form 'm/d/yy'"}, 400))

        if "description" in data and "title" in data:
            return Task(
                title = data["title"],
                description = data["description"],
                completed_at = data["datetime"]
            )
        else:
            return False