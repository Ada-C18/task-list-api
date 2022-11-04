from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)

    # not sure if this should be a column- we will
    # want to calculate this ourselves given completed_at
    # is_complete = db.Column(db.Boolean)

    # not sure if this should be a column- we need the data
    # behind the scenes, but don't want to share it with the client
    completed_at = db.Column(db.DateTime, nullable=True)
    