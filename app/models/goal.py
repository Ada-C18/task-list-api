from app import db
from flask import abort, make_response


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task")

    def to_dict(self):
        goal_dict = {
            "id" : self.id,
            "title" : self.title,
            }
        return goal_dict

    def get_tasks(self):
        response = []
        for task in self.tasks:
            response.append(task.to_dict())
        return response

    def get_task_ids(self):
        response = []
        for task in self.tasks:
            response.append(task.id)
        return response

    
    
    @classmethod
    def from_dict(cls, request_body):
        try:
            goal = Goal(title = request_body["title"]) 
            return goal
        except:
            abort(make_response({"details" : "Invalid data"}, 400))

    @classmethod
    def validate_goal_id(cls, goal_id):
        try:
            goal_id = int(goal_id)
        except:
            abort(make_response({"message" : f"goal id: {goal_id} is invalid"}, 400))
    
        goal = Goal.query.get(goal_id)

        if not goal:
            abort(make_response({"message" : f"goal {goal_id} not found"}, 404))
    
        return goal
        