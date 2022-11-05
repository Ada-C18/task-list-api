from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
<<<<<<< HEAD
=======

>>>>>>> 36023d35d759cf2e11d9bda3d9c6954aa5b1f05e
