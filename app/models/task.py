from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable =True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable = True)
    goal = db.relationship("Goal", back_populates="tasks")
    
    def to_dict(self):

        return dict(
            id = self.id,
            title = self.title,
            description = self.description,
            is_complete = False)

    @classmethod
    def from_dict(cls, data_dict):
        return Task(title = data_dict["title"],
                    # completed_at = data_dict["completed_at"],
                    description = data_dict["description"]
                    )
