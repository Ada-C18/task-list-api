from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #add autoincrement=True?
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"],
                        completed_at=task_data["completed_at"])
    
    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at
        }