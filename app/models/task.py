from app import db
from flask import jsonify, abort, make_response


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)
    


    def is_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True
    
    def to_dict(self):
        task_dict = {
            "id" :self.id,
            "title" : self.title,
            "description" : self.description, 
            "is_complete" : self.is_complete()
            }
        return task_dict

    @classmethod
    def from_dict(cls, request_body):
        try:
            task = Task(title = request_body["title"],
                        description = request_body["description"]) 
            return task
        except:
            abort(make_response({"details" : "Invalid data"}, 400))

    @classmethod
    def validate_task_id(cls, task_id):
        try:
            task_id = int(task_id)
        except:
            abort(make_response({"message" : f"task id: {task_id} is invalid"}, 400))
    
        task = Task.query.get(task_id)

        if not task:
            abort(make_response({"message" : f"task {task_id} not found"}, 404))
    
        return task
        