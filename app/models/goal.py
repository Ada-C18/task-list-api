from app import db
from sqlalchemy.orm import relationship


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = relationship("Task", back_populates="goal", lazy=True)

    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,}
    @classmethod
    def from_dict(cls, data):
        if "title" in data:
            return Goal(
                title = data["title"],
            )
        else:
            return False