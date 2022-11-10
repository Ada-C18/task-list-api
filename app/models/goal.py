from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title= db.Column(db.String, nullable=False)
    tasks = db.relationship("Task", back_populates="goal", lazy= True)

    @classmethod
    def from_dict(cls,data_dict):
        return cls(
            title=data_dict["title"]
            )

    def to_dict(self, tasks=False):
        if not self.tasks and tasks==False:
            return dict(
                id=self.id,
                title=self.title,
        )
        return dict(
                id=self.id,
                title=self.title,
                tasks=[task.to_dict(goal=True) for task in self.tasks]
        )