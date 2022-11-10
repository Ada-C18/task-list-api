from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #add autoincrement=True?
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=None)
        return new_task
    
    def is_complete(task_data):
        if task_data.completed_at == None:
            return False
        else:
            return True
    
    def to_dict(self):
        task = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete()
            }
        if self.goal_id:
            task["goal_id"] = self.goal_id
        return task