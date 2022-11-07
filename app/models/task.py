from app import db

class Task(db.Model):
    id =           db.Column(db.Integer, primary_key=True)
    title =        db.Column(db.String,    nullable=False)
    description =  db.Column(db.String,    nullable=True)
    completed_at = db.Column(db.DateTime,  nullable=True,  default=None)
    is_complete =  db.Column(db.Boolean,   nullable=True, default=False)

    def create_dict(self):
        task_as_dict = {}
        task_as_dict["id"] = self.id  
        task_as_dict["title"] = self.title
        task_as_dict["description"] = self.description
        task_as_dict["is_complete"] = self.is_complete
        
        return task_as_dict
    
    def update(self, req_body):
        self.title = req_body["title"]
        self.description = req_body["description"]

    @classmethod
    def new_instance_from_dict(cls, req_body):
        new_dict = cls(
                        title = req_body["title"],
                        description = req_body["description"],
                        completed_at = req_body["completed_at"]
                        )
        return new_dict
