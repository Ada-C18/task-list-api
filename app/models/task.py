from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict_post_put(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False
        }

    def to_dict_get_patch(self):
        if not self.completed_at:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": False
            }
        else:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": True
                }

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=None
        )
        return new_task