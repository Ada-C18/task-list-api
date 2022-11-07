from app import db
from flask import abort, make_response
from flask import jsonify


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    
    @classmethod
    def from_dict(cls, data_dict):
        return cls(title=data_dict["title"],
        description=data_dict["description"],
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if not self.completed_at else True    
        }
    
    def update(self,req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
        except KeyError as error:
            abort(make_response(jsonify(dict(details="Invalid data")), 400))
    
