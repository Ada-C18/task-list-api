from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship('Task', back_populates='goal', lazy=True)

    def to_dict(self):
        return {
                "id": self.goal_id,
                "title": self.title,
                # "task_ids": self.get_task_list()
            }
    
    def to_dict_relationship(self):
        return {
                "id": self.goal_id,
                "title": self.title,
                "tasks": self.get_task_list()
            }
    
    def get_task_list(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.to_dict_relationship())
        return list_of_tasks