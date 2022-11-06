from app import db


class Task(db.Model):
    # __tablename__ = "tasks"
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True)
    # goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self, determine_completion):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": determine_completion(self)
            }
    
    def to_dict_with_goal(self, determine_completion):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": determine_completion(self),
            "goal_id": self.goal_id
            }

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
        description=task_data["description"])

        return new_task