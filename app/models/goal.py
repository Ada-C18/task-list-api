from app import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal", lazy=True)


    @classmethod
    def to_dict(cls, self):
        return {
            "id": self.id,
            "title":self.title
        }
    

    @classmethod
    def create_from_dict(cls, request_body):
        return Goal(
            title=request_body["title"]
        )


    @classmethod
    def update_from_dict(cls, self, request_body):
        self.title = request_body["title"]