from app import db


class Goal(db.Model):
    __tablename__ = "goal"
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)
    

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
            }

    def get_list_of_tasks():
        list_of_tasks = []
        for task in self.tasks:
            list_of_tasks.append(task.to_dict)
        return list_of_tasks