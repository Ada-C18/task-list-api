from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    
    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
            # "tasks": [task.task_id for task in self.tasks]
        }
    
    @classmethod
    def from_dict(cls, goal_data):
        new_goal = Goal(title=goal_data["title"])

        return new_goal

    def get_task_list(self):
        '''
        return a list of tasks associated with goal
        '''
        list_of_tasks = []

        for task in self.tasks:
            if task.goal_id:
                task_dict = task.to_dict()
                task_dict["goal_id"] = task.goal_id
                list_of_tasks.append(task_dict)
                break
            list_of_tasks.append(task.to_dict())

        return list_of_tasks