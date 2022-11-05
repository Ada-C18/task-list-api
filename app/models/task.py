from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"))
    goal = db.relationship("Goal", back_populates="tasks")
    

    @classmethod
    def to_dict(cls, self):
        return {
            "id": self.id,
            "title":self.title,
            "description": self.description,
            "is_complete": True if self.completed_at else False
        }
    

    @classmethod
    def create_from_dict(cls, request_body):
        return Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )
    

    @classmethod
    def update_from_dict(cls, self, request_body):
        self.title = request_body["title"]
        self.description = request_body["description"]