from app import db
# from flask import abort, make_response


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.goal_id")) #can this have the same name as the primary key column?
    goal = db.relationship("Goal", back_populates="tasks")

    # def to_dict(self):
    #     task_as_dict = {}
    #     task_as_dict["task_id"]: self.id
    #     task_as_dict["title"]: self.title
    #     task_as_dict["description"]: self.description
    #     task_as_dict["completed_at"]: self.completed_at

    #     return task_as_dict

    # @classmethod
    # def from_dict(cls, request_body):
    #     new_task = Task(
    #         title=request_body["title"],
    #         description=request_body["description"],
    #         completed_at=request_body["completed_at"]
    #     )

    #     return new_task
    
    # def update(self,request_body):
    #     try:
    #         self.name=request_body["title"]
    #         self.description=request_body["description"]
    #         self.completed_at=request_body["completed_at"]
    #     except KeyError as error:
    #         abort(make_response({'message':f"Missing attribute: {error}"}))