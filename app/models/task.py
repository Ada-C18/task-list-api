from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    completed_at = db.Column(db.DateTime, nullable=True) # default value is None until we change it later
    is_complete = db.Column(db.Boolean, default=False) # check later if default=False works