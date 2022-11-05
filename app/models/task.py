from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    # take a look at this - is this ok or need to use nullable=True?
    completed_at = db.Column(db.DateTime, default=None)

    @property
    def is_complete(self):
        return bool(self.completed_at)
