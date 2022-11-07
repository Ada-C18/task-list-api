from app import db
from sqlalchemy.orm import relationship


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.String, nullable=True)
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
        if "description" in data and "title" in data:
            return Task(
                title = data["title"],
                description = data["description"],
                completed_at = None
            )
        else:
            return False