from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)

    def to_dict(self):
        goals_dict = {
            "id" : self.goal_id,
            "title" : self.title            
        }
        
        return goals_dict

