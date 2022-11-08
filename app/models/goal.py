from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def to_response(self):
        return {
            "goal": self.to_dict()
        }

    def to_dict(self):
        return {    
                "id":self.goal_id,
                "title":self.title
                #"description":self.description,
                
                #"is_complete": True if self.completed_at else False
                
        }
        