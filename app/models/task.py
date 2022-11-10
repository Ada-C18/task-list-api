from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default=None) 
    is_complete = db.Column(db.Boolean, default=False) #until Wave 3
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship("Goal", back_populates="tasks")

    def to_dict(self):
        if self.goal_id:
            return {"id": self.id,
                    "title": self.title,
                    "description": self.description,
                    "is_complete": self.is_complete,
                    "goal_id": self.goal_id   
            }
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.is_complete 
        }
    
    def update(self, req_body):
        self.title=req_body["title"],
        self.description=req_body["description"],
        # self.completed_at=req_body["completed_at"],
        # self.is_complete=req_body["is_complete"]

    @classmethod
    def from_dict(cls, task_data):
        return Task(title=task_data["title"], description=task_data["description"])