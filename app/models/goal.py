from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks= db.relationship("Task",back_populates="goal",lazy=True)
    

    @classmethod
    def from_dict(cls, data_dict):  # GET/READ

        return cls(title=data_dict["title"])

    def to_dict(self):  # POST/CREATE

        return dict(id=self.id,
                    title=self.title)