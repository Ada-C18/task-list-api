from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True, default = None)

    @classmethod
    def from_dict(cls, data_dict):
        if "completed_at" in data_dict:
            return cls(title = data_dict["title"], 
            description = data_dict["description"],
            completed_at = data_dict["completed_at"])
        else:
            return cls(title = data_dict["title"], 
            description = data_dict["description"])

    
    def to_dict(self):
        if self.completed_at:
            flag = True
        else:
            flag = False
        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = flag
        )