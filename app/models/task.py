from app import db
from flask import abort, make_response
import datetime


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = True)
    


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
        if self.goal_id != None:
            task_dict.update({"goal_id" : self.goal_id})
        return task_dict
    
    def mark_complete(self):
        if self.is_complete():
            pass
        else:
            self.completed_at = datetime.datetime.now()
        
    def mark_incomplete(self):
        if not self.is_complete():
            pass
        else:
            self.completed_at = None           

    @classmethod
    def from_dict(cls, request_body):
        try:
            task = Task(title = request_body["title"],
                        description = request_body["description"]) 
            return task
        except:
            abort(make_response({"details" : "Invalid data"}, 400))
