from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime,nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable = True)
    goal = db.relationship("Goal", back_populates = "tasks")

    def to_dict(self):
        task = {
            "id":self.task_id,
            "title":self.title,
            "description":self.description ,
            # "is_complete":bool(self.completed_at)
            "is_complete":True if self.completed_at else False    
        }
        if self.goal_id:
            task["goal_id"]=self.goal_id

        return task     


    @classmethod
    def from_dict(cls, task_dict):
        return cls(
            title = task_dict["title"],
            description = task_dict["description"]    
        )    
