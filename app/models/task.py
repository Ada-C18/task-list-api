from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime) # todo: nullable default=None?
    is_complete: db.Column(db.Boolean) # False until wave 3

    def to_dict(self):
        return {
            "task_id":self.task_id,
            "title":self.title,
            "description":self.description,
            "completed_at": self.completed_at,
            "is_complete": self.is_complete
        }