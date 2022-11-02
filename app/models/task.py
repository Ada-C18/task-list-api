from app import db

# create the table with attributes
# after created, run flask db init, flask db migrate, flask db upgrade
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
