from app import db


class Task(db.Model):

    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    
    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                    description=task_data["description"])
        return new_task

    
    def to_dict(self):
        if not self.completed_at:
            self.completed_at = False
        elif self.completed_at:
            self.completed_at=True
        return dict(
            id = self.task_id,
            title = self.title, 
            description = self.description, 
            is_complete=self.completed_at
            )

#"is_complete": True if self.completed_at == True else False

