from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        if self.completed_at:
            complete = True
        else:
            complete = False
        return { "id": self.id,
        "title": self.title,
        "description": self.description,
        "is_complete": complete,
        }

