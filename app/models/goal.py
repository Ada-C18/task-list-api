from app import db

#Parent 
class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal")

def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }

@classmethod
def from_dict(cls, request_body):
    return cls(
        title=request_body["title"]
    )
