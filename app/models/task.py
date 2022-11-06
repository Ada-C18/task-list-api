from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    is_completed = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "is_completed": self.is_completed,
            "description": self.description
        
        }


