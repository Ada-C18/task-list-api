from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)


    @classmethod
    def to_dict(cls, self):
        return {
            "id": self.id,
            "title":self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
    

    @classmethod
    def create_from_dict(cls, request_dict):
        return Task(
            title=request_dict["title"],
            description=request_dict["description"],
            completed_at=None
        )