from app import db
from flask import jsonify


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates='goal', lazy=True)

    def g_json(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def to_dict(self):
        as_dict = {}
        as_dict["id"] = self.id
        as_dict["title"] = self.title

        return as_dict

