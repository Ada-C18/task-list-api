from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
        }

    # def to_dict finish to dict with tasks 
    
    def get_task_list(self):
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append({
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            })
        return list_of_tasks

    @classmethod
    def from_dict(cls, cls_dict):
        return cls(
        title = cls_dict["title"]
        )