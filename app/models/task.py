from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }

    def sort(self, list_of_dict_tasks):
        sorted_list = sorted(list_of_dict_tasks.items(), key=lambda x:x[1])
        convert_to_dict = dict(sorted_list)
        return convert_to_dict