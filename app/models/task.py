from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)
    # goal_id = db.Column(db.Integer,db.ForeignKey('goal.id'))

    def to_dict(self):
        if self.completed_at is None:
            task_dict = {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": False
            }
        else: 
            task_dict = {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": True
            } 
        return task_dict