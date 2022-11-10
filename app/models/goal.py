from app import db

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    lazy = db.Column(db.Boolean, default=True)
    tasks = db.relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }
    
    def update(self, req_body):
        self.title=req_body["title"]

    @classmethod
    def from_dict(cls, goal_data):
        return Goal(title=goal_data["title"])