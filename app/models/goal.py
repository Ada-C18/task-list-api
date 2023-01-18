from app import db
from .task import Task

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80)) 
    task_rel = db.relationship("Task", back_populates="goal", lazy=True) 

    def goal_dict(self):
            return {
                "id": self.goal_id,
                "title": self.title}
    
    @classmethod
    def from_dict(cls, goal_data):
        goal_class = cls(title=goal_data["title"])
        return goal_class
        