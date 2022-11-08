from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    def create_dict(self):

        new_dict = {
        "id": self.task_id,
        "title": self.title,
        "description": self.description,
        "is_complete": self.completed_at
        }

        if self.completed_at is None:
            new_dict["is_complete"] = False
        else:
            new_dict["is_complete"] = True

        return new_dict
