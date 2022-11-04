from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)  


    def to_dict(self):
        return {
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": False 
        }

    #create a different helper function, one to get one task, another to get all tasks----