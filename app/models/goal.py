from app import db
from flask import abort, make_response, jsonify

# One goal can have multiple tasks
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    

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


        


