from app import db

#Child
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")


    def to_dict(self):
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at) 
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id

        return task_dict
    
    @classmethod
    def from_dict(cls, request_body):
        return cls(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )


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