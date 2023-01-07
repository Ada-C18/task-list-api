from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def create_dict(self, tasks=False):
            goal_as_dict = {}
            goal_as_dict["id"] = self.goal_id  
            goal_as_dict["title"] = self.title
            
            if tasks:
                goal_as_dict["tasks"] = [task.create_dict() for task in self.tasks]
            
            return goal_as_dict

    def patch(self, req_body):
        self.title = req_body.get("title")

    @classmethod 
    def new_instance_from_dict(cls, req_body):
        new_dict = cls(
                        title = req_body["title"],
                        )
        return new_dict

