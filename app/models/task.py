from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return dict(
            id = self.task_id,
            title = self.title,
            description = self.description,
            is_complete = False)

    @classmethod
    def from_dict(cls, data_dict):
        if "completed_at" in data_dict:
            return Task(title = data_dict["title"],
                    description = data_dict["description"],
                    completed_at = data_dict["completed_at"])
                    

        else:
            return Task(title = data_dict["title"],
                    description = data_dict["description"])
                

        





