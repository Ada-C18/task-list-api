from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    # completed_at = db.Column(db.DateTime, nullable=True, default=None)
    # is_complete = db.Column(db.Boolean, default = False)

    def to_dict(self):
        # if self.completed_at is None:
        task_dict = {
                "id" : self.task_id,
                "title": self.title,
                "description" : self.description,
                # "is_complete" : False
                "is_complete" : True if self.completed_at else False
            }

        return task_dict
        
        
        # if self.completed_at is None:
        #     task_dict = {
        #         "id" : self.task_id,
        #         "title": self.title,
        #         "description" : self.description,
        #         # "is_complete" : False
        #         "is_complete" : True if self.completed_at else False
        #     }
        
        # else:
        #     task_dict = {
        #         "id" : self.task_id,
        #         "title": self.title,
        #         "description" : self.description,
        #         "complete_at" : self.completed_at
        # }
        # return task_dict
        