from app import db
import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Title',db.String(80), index = True, unique = False) 
    description  = db.Column('Description', db.String(80), index = True, unique = False) 
    completed_at = db.Column('Completed On', db.DateTime, index = True, unique = False, nullable = True)
    
# datetime that has the date that a task is completed on. 
# **Can be _nullable_,** and contain a null value. A task with a `null` value for `completed_at` has not been completed.
# When we create a new task, `completed_at` should be `null` AKA `None` in Python.


def __repr__(self):
    return f'''<Task (Title: {self.title}
                Description: {self.description}
                Completed: {self.completed_at})'''