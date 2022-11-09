from app import db

#Child
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    # def to_dict(self):
    #     task_as_dict = {}
    #     task_as_dict["id"] = self.task_id
    #     task_as_dict["title"] = self.title
    #     task_as_dict["description"] = self.description
        
    #     #Check to see if truthy
    #     if completed_at:
    #         pass
        
    #     return task_as_dict

    # @classmethod
    # def from_dict(cls, task_data):
    #     new_task = Task(title=task_data["title"],
    #                     description=task_data["description"])
    #     return new_task


# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         response_body = {
#             "message": f"{cls.__name__} id {model_id} is invalid."
#         }

#         abort(make_response(jsonify(response_body), 400))
    
#     model = cls.query.get(model_id)

#     if model is None:
#         response_body = {
#             "message": f"{cls.__name__} {model_id} does not exist."
#         }

#         abort(make_response(jsonify(response_body), 404))
    # return model