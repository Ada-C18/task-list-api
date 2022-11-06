from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    # helper function to structure request response json
    def make_task_dict(self):
        task_dict = {"id": self.task_id,
        "title": self.title,
        "description": self.description}

        if not self.completed_at:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True
            # task_dict["completed_at"] = task.completed_at
        
        return task_dict
