from app import db 
from flask import abort, make_response
# import datetime
# from sqlalchemy import Column, Integer, DateTime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        } 
        
    @classmethod
    def from_dict(cls, req_body):
        return cls(
            title=req_body['title'],
            description=req_body['description']
            # is_complete=req_body['is_complete']
        )
    
# def update(self, req_body):
#     try:
#         self.title = req_body["title"],
#         self.description = req_body["description"],
#         self.complete = req_body["completed_at"]
#     except KeyError as error:
#         abort(make_response({'message': f"Missing attribute: {error}"}))