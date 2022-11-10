from app import db
from .task import Task

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    def goal_to_dict(self, tasks=False):
        if not self.tasks and tasks==False:
            return {
                'id': self.goal_id,
                'title': self.title
                }
        else:
            return {
                'id': self.goal_id,
                'title': self.title,
                'tasks': [task.to_dict(goal=True) for task in self.tasks]
                }

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = cls(title=goal_data["title"])
        return new_goal