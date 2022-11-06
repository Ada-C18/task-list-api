from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"],
        description=data_dict["description"]
        )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at == None else self.completed_at,    
        }
    

    
