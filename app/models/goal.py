from app import db
from flask import current_app

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy= True)

    def to_json_goal(self):
        return{
            "id": self.id,
            "title": self.title
        }