from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")

    def create_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.task_id  
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description

        task_as_dict["is_complete"] = bool(self.completed_at)
        
        if self.goal_id:
            task_as_dict["goal_id"] = self.goal_id
        
        return task_as_dict

    def patch(self, req_body):
        self.title = req_body.get("title")
        self.description = req_body.get("description")
        self.goal_id = req_body.get("goal_id")

    @classmethod 
    def new_instance_from_dict(cls, req_body):
        new_dict = cls(
                        title = req_body["title"],
                        description = req_body["description"],
                        goal_id = req_body.get("goal_id")
                        )
        return new_dict
