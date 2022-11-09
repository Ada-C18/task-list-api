from app import db
from flask import Blueprint, jsonify, abort, make_response, request

#Parent 
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
            return {
                "id": self.goal_id,
                "title": self.title
            }

    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"]
        )
    def update(self, req_body):
            try: 
                self.title = req_body["title"]
            except KeyError:
                abort(make_response({"details": "Invalid data"}, 400))