from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(2600))
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        if self.completed_at:
            complete = True
        else: 
            complete = False

        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = complete

        return task_as_dict