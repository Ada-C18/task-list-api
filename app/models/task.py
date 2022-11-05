from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return{
            "title" : self.title,
            "description" : self.description,
            "completed at" : self.completed_at
        }
    
    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title = req_body['title'],
            description = req_body['description'],
            completed_at = req_body['completed_at']
        )