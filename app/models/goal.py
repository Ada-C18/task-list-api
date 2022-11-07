from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal")

    def to_dict(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.to_dict())
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": list_of_tasks
        }

    @classmethod
    def from_dict(goal_dict):
        return Goal(
            title = goal_dict["title"],
            tasks = goal_dict["tasks"]
        )

    def get_task_list(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.to_dict())
        return list_of_tasks