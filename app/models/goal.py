from app import db
from flask import abort, make_response


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict_goals(self):
        return { "goal":{
                "id":self.goal_id,
                "title": self.title}
                }

    @classmethod
    def from_dict_goals(cls, goal_data):
        try:
            new_goal = Goal(title=goal_data["title"])
        except KeyError as error: 
            abort(make_response({"details":"Invalid data"},400))
        return new_goal

    def update_goal(self, req_body):
        try:
            self.title = req_body["title"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"},400))
