from app import db
from flask import abort, make_response, jsonify


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)


@classmethod
def from_dict(cls, data_dict):
    return cls(title=data_dict["title"])

def to_dict(self):
    return {
        "id": self.id,
        "title": self.title    
    }

def update(self,req_body):
    try:
        self.title = req_body["title"]
    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))