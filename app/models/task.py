from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.String, nullable=True, default=None)
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    goal = db.relationship("Goal", back_populates="tasks", lazy= True)

    @classmethod
    def from_dict(cls,data_dict):
        return cls(
            title=data_dict["title"],
            description=data_dict["description"]
            )

    def to_dict(self, goal=False):
        if not self.completed_at:
            self.completed_at = False
        else:
            self.completed_at = True
        if self.goal_id:
            return dict(
            id=self.id,
            goal_id = self.goal_id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at
        )
        return dict(
            id=self.id,
            title=self.title,
            description=self.description,
            is_complete=self.completed_at
        )
