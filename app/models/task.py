from app import db


class Task(db.Model):
    task_id =           db.Column(db.Integer, primary_key=True)
    task_title =        db.Column(db.String,    nullable=False)
    task_description =  db.Column(db.String,    nullable=True)
    task_completed_at = db.Column(db.DateTime,  nullable=True,  default=None)
    task_is_completed = db.Column(db.Boolean,   nullable=False, default=False)

