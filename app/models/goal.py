from app import db
import sqlalchemy as sa


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_title = db.Column(db.String, nullable=False)

    def to_dict():
        return{
            "id": self.goal_id,
            "title": self.goal_title
        }
    
    def from_dict(self):
        return {
            "title": self.goal_title
        }