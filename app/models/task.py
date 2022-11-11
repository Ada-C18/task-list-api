from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)


    def to_dict(self):
        if self.goal_id:
            return dict(
                id = self.task_id,
                title = self.title,
                description = self.description,
                is_complete = False if self.completed_at is None else True,
                goal_id = self.goal_id)

        else:
            return dict(
                id = self.task_id,
                title = self.title,
                description = self.description,
                is_complete = False if self.completed_at is None else True)

    @classmethod
    def from_dict(cls, data_dict):
        if "completed_at" in data_dict:
            return Task(title = data_dict["title"],
                    description = data_dict["description"],
                    completed_at = data_dict["completed_at"])
                    

        else:
            return Task(title = data_dict["title"],
                    description = data_dict["description"])
                

        





