from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, null=True) # is this correct? null=True
    #Can be nullable, and contain a null 
    # value. A task with a null value for completed_at has not been completed. 
    # When we create a new task, completed_at should be null AKA None in Python.


# Wave 1 CRUD
# Tasks are entities that describe a task a user wants to complete. They contain a:
# title to name the task
# description to hold details about the task
# an optional datetime that the task is completed on
# Our goal for this wave is to be able to create, read, update, and delete 
# different tasks. We will create RESTful routes for this different operations.