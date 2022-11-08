from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_dict(self):
        goals_dict = {
            "goal_id" : self.goal_id,
            "title" : self.title            
        }
        
        return goals_dict

