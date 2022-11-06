from app import db
from flask import make_response, abort
import datetime

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    one_goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id"), nullable=True) #goal is the parent's table name in the DB
    one_goal = db.relationship("Goal", back_populates="many_tasks")

    @classmethod
    def instance_from_json(cls, task_req_body):
        try:
            if "is_complete" in task_req_body:
                completed_at_datetime = task_req_body["is_complete"]
                if not type(completed_at_datetime) == type(datetime.datetime.now()):
                    abort(make_response({"message":f"Invalid datetime format: {completed_at_datetime}"}, 400))
                new_task = Task(title=task_req_body["title"],
                            description=task_req_body["description"],
                            completed_at = completed_at_datetime)
            else:
                new_task = Task(title=task_req_body["title"],
                            description=task_req_body["description"],
                            completed_at = None)
            return new_task
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))

    def to_dict(self):
        task_as_dict = {}
        if self.one_goal:
            if self.completed_at == None:
                task_as_dict["id"] = self.task_id
                task_as_dict["title"] = self.title
                task_as_dict["description"] = self.description
                task_as_dict["is_complete"] = False
                task_as_dict["goal_id"] = self.one_goal_id
            else: 
                task_as_dict["id"] = self.task_id
                task_as_dict["title"] = self.title
                task_as_dict["description"] = self.description
                task_as_dict["is_complete"] = True
                task_as_dict["goal_id"] = self.one_goal_id
        else:    
            if self.completed_at == None:
                task_as_dict["id"] = self.task_id
                task_as_dict["title"] = self.title
                task_as_dict["description"] = self.description
                task_as_dict["is_complete"] = False
            else: 
                task_as_dict["id"] = self.task_id
                task_as_dict["title"] = self.title
                task_as_dict["description"] = self.description
                task_as_dict["is_complete"] = True
        return task_as_dict

    def update(self, req_body):
        try:
            if "is_complete" in req_body:
                completed_at_datetime = req_body["is_complete"]
                if not type(completed_at_datetime) == type(datetime.datetime.now()):
                    abort(make_response({"message":f"Invalid datetime format: {completed_at_datetime}"}, 400))
                self.title = req_body["title"]
                self.description = req_body["description"]
                self.completed_at = req_body["is_complete"]
            else:
                self.title = req_body["title"]
                self.description = req_body["description"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"}, 400))

    def validate_datetime(self):
        if not type(self.completed_at) == type(datetime.datetime.now()):
            abort(make_response({"message":f"Invalid datetime format: {self.completed_at}"}, 400))