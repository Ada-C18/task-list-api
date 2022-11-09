from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=True)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            }

    def goal_to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": self.get_tasks_list_whole()
        }

    def get_tasks_list_ids(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.id)
        return list_of_tasks

    def get_tasks_list_whole(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.to_dict_with_goal_id())
        return list_of_tasks