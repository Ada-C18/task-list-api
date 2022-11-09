from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is complete"] = False

        return task_as_dict
        
        
        
        # return dict(
        #     task = dict(
        #         id = self.id,
        #         title = self.title,
        #         description = self.description,
        #         is_complete = False
        #     )
        # )