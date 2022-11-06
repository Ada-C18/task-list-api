from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        tasks_as_dict = {}
        tasks_as_dict["id"] = self.task_id
        tasks_as_dict["title"] = self.title
        tasks_as_dict["description"] = self.description
        if self.completed_at:
            tasks_as_dict["is_complete"] = True
        else:
            tasks_as_dict["is_complete"] = False

        return tasks_as_dict