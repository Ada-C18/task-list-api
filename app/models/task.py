from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) 
    is_complete = db.Column(db.Boolean, default=False) #until Wave 3

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            #"completed_at": self.completed_at,
            "is_complete": self.is_complete 
        }
    
    def update(self, req_body):
        self.title=req_body["title"],
        self.description=req_body["description"],
        # self.completed_at=req_body["completed_at"],
        # self.is_complete=req_body["is_complete"]

    @classmethod
    def from_dict(cls, task_data):
        new_task = Task(title=task_data["title"],
                        description=task_data["description"])
                        #completed_at=task_data["completed_at"])
        return new_task

#From Planet

#     @classmethod   
#     def from_json(cls, req_body):
#         return cls(
#             title= req_body["title"],
#             completed_at= req_body["completed_at"],
#             description= req_body["description"]
#         )
