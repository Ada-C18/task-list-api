from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable = True)

    def to_dict(self):
        if self.completed_at is not None:
            completed = True
        elif self.completed_at is None:
            completed = False
        return {"task": {
        "id":self.task_id, 
        "title":self.title, 
        "description": self.description,
        "is_complete": completed}}

    def to_dict_all_tasks(self):
        return {
        "id":self.task_id, 
        "title":self.title, 
        "description": self.description,
        "is_complete": False}