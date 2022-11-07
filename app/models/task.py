from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.String, nullable=True)

    def to_dict(self):
        is_complete = False if self.completed_at == None else True
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": is_complete,
        }
    @classmethod
    def from_dict(cls, data):
        if "description" in data and "title" in data:
            return Task(
                title = data["title"],
                description = data["description"],
                completed_at = None
            )
        else:
            return False