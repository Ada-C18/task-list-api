from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self, tasks=False):
        goal = {
            "id": self.goal_id,
            "title": self.title,
        }
        if tasks:
            goal["tasks"] = [task.to_dict() for task in self.tasks]
        return goal

    def update(self, **kwargs):
        for key in kwargs:
            if key in ("title"):
                setattr(self, key, kwargs[key])
            if key == "task_id":
                self.add_tasks(kwargs[key])

    def add_tasks(self, task_ids=None, tasks=None):
        from app.models.task import Task

        self.tasks += tasks or Task.query.filter(Task.task_id.in_(task_ids)).all()
