from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.breed,
            "is_complete": True if self.completed_at else False
        }