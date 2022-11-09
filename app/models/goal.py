from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):
        goal_as_dict = {}
        goal_as_dict["id"]=self.goal_id
        goal_as_dict["title"]=self.title
        return goal_as_dict

    # def to_dict_response(self):
    #     return {
    #         "goal_id":self.goal_id,
    #         "title":self.title,
    #         "description": self.description,
    #         "is_complete": self.is_complete
    #     }

    # def get_tasks_list(self):
    #     list_of_tasks = []
    #     for task in self.tasks:
    #         list_of_tasks.append(task.to_dict)
    #     return list_of_tasks

    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])
        return new_goal