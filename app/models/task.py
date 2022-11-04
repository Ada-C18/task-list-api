from app import db
from flask import make_response, abort

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def instance_from_json(cls, task_req_body):
        try:
            # new_task = Task(title=task_req_body["title"],
            # description=task_req_body["description"],
            # completed_at = task_req_body["is_complete"])
            if "is_complete" in task_req_body:
                new_task = Task(title=task_req_body["title"],
                            description=task_req_body["description"],
                            completed_at = task_req_body["is_complete"])
            else:
                new_task = Task(title=task_req_body["title"],
                            description=task_req_body["description"],
                            completed_at = None)
            return new_task
        except KeyError:
            abort(make_response({"details": "Invalid data"}, 400))

    def to_dict(self):
        task_as_dict = {}
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
            self.title = req_body["title"]
            self.description = req_body["description"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"}, 400))
    
    # def mark_complete(self):
    #     try:
    #         self.completed_at = datetime.datetime.now()
    #     except KeyError as error:
    #         abort(make_response({"message": f"Missing attribute: {error}"}, 400))