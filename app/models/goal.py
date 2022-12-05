from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def from_instance_to_dict(self, tasks = False):
        instance_dict = {
            "id": self.goal_id,
            "title" : self.title,
        }
        if tasks:
            instance_dict["tasks"] = [task.from_instance_to_dict() for task in self.tasks]
        return instance_dict


    @classmethod
    def from_dict_to_instance(cls, goal_data):
        
        new_goal = Goal(title=goal_data["title"])
        return new_goal
