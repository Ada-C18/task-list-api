from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), index = True, unique = False) 
    description  = db.Column(db.String(80), index = True, unique = False) 
    completed_at = db.Column(db.DateTime, index = True, unique = False, nullable = True)
    
# datetime that has the date that a task is completed on. 
# **Can be _nullable_,** and contain a null value. A task with a `null` value for `completed_at` has not been completed.
# When we create a new task, `completed_at` should be `null` AKA `None` in Python.
