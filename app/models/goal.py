from app import db
from flask import Blueprint, make_response, request, jsonify, abort, request



class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "title": self.title,
            "id": self.goal_id
        }

    @classmethod
    def from_json(cls, req_body):
        return cls(
            title=req_body['title']
        )

    def update(self,req_body):
        try:
            self.title = req_body["title"]
        except KeyError as error:
            abort(make_response({'message': f"Missing attribute: {error}"}))

    def to_new_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None,
            "id": self.task_id,
            "goal_id": self.goal_id
        }
