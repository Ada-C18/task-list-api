from app import db
from datetime import datetime
from flask import abort, make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String)
    description=db.Column(db.String)
    completed_at=db.Column(db.DateTime)
    is_completed=db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        
        return dict(
            id= self.id,
            title= self.title,
            description= self.description,
            is_complete=False
            
    )
