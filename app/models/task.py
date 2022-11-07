from app import db
from flask import jsonify


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    


    def is_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True
    
    def to_dict(self):
        task_dict = {
            "id" :self.id,
            "title" : self.title,
            "description" : self.description, 
            "is_complete" : self.is_complete()
            }
        return task_dict
