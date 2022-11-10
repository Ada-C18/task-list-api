from app import db
import sqlalchemy as sa


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)

    def from_dict(self):
        return {
            "title": self.title
        }

    def to_dict(self):
        return{
            "id": self.goal_id,
            "title": self.title
        }
    
    