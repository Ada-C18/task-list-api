from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.String)
    description= db.Column(db.String)
    completed_at= db.Column(db.DateTime ,nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'))
    goal = db.relationship('Goal', back_populates='tasks')

    def to_dict(self):
        if self.goal_id is None:
            return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": True if self.completed_at else False,          
            }
        else:
            return {
                "id":self.id,
                "title":self.title,
                "description":self.description,
                "is_complete": True if self.completed_at else False, 
                "goal_id": self.goal_id          
            }




