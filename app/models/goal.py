from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy = True)

    def to_dict(self):
        goal_dict = {
            "id": self.goal_id,
            "title": self.title,
        }
        return goal_dict

    def get_task_ids(self):
        task_ids = [task.task_id for task in self.tasks] #get_task_idstask_ids = []
    #     for task in self.task_items:
    #         task_ids.append(task.task_id)
        return task_ids