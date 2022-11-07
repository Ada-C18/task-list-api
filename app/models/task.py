from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)


    def to_dict(self):
        #check data_dict has all valid task attributes 
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete
        }
        return task_dict