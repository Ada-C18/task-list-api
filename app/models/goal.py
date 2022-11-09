from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True,  autoincrement = True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates = "goal")

    @classmethod
    def from_json(cls, req_body):
        return cls(
                title = req_body["title"]
        )

    def to_dict(self):
        return(
            {
                "goal": {
                    "id": self.goal_id,
                    "title": self.title
                }
            }
        )

    def update(self, req_body):
        try:
            self.title = req_body["title"]
        except KeyError as error:
            raise error