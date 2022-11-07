from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    # title= db.Column(db.String, nullable=False)
    # description = db.Column(db.Integer, primary_key=True)
    # completed_at = db.Column(db.Integer, primary_key=True)