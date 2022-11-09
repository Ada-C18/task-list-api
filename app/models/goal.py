from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    def to_dict(self):

        return {
            "id": self.goal_id,
            "title" : self.title,
        }

    @classmethod
    def from_dict(cls, goal_data):
        
        new_goal = Goal(title=goal_data["title"])
        return new_goal

    
    # def to_dict_goal(self):

    #     return {
    #         "id" : self.goal_id,
    #         "title": self.title,
    #         "tasks": [
    #             {
    #                 "id": self.goal.tasks.task_id,
    #                 "goal_id": self.goal.tasks.goal_id,
    #                 "title": self.goal.tasks.title,
    #                 "description": self.goal.tasks.description,
    #                 "is_complete": bool(self.tasks.completed_at)
    #             }
    #         ]
    #     }

    # def task_list_goal(self):
    #     task_list = []
    #     for task in self.tasks:
    #         task_list.append({
    #                 "id": task.task_id,
    #                 "goal_id": task.goal_id,
    #                 "title": task.title,
    #                 "description": task.description,
    #                 "is_complete": bool(task.completed_at)})