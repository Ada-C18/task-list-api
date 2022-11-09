from app import db
import datetime


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    is_complete = db.Column(db.Boolean, default=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def create_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.task_id  
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete
        
        return task_as_dict

    def update(self,req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

    @classmethod 
    def new_instance_from_dict(cls, req_body):
        new_dict = cls(
                        title = req_body["title"],
                        description = req_body["description"],
                        # is_complete = req_body["is_complete"]
                        )
        return new_dict
