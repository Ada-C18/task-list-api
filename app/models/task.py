from app import db


class Task(db.Model):
    __tablename__ = "task"
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    # tasks is the list of tasks created for each goal - new parameter

    def is_complete(self):
        return self.completed_at is not None
        

    def to_dict(self):
        dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
        }
        
        if self.goal_id:
            dict["goal_id"] = self.goal_id

        return dict


    # @classmethod
    # def from_dict(cls, task_data):
    #     new_task = Task(title=task_data["title"], description=task_data["description"], completed_at=task_data["completed_at"])
    #     return new_task
