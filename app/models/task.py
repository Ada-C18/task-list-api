from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates = "tasks")


    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "goal_id": self.goal_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }

        if self.is_complete is None:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True

        if self.goal_id is None:
            task_dict.pop("goal_id")
  
        return task_dict



        
