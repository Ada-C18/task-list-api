from app import db


# create the table with attributes
# after created, flask db migrate, flask db upgrade
class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'),nullable=True)
    goal = db.relationship("Goal", back_populates="tasks")
    

    def return_body(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.check_complete_or_not()
        }

   
    @classmethod
    def from_dict(cls, data_dict):
        if "title" in data_dict and\
            "description" in data_dict and\
            "completed_at" in data_dict:
            new_obj = cls(
                title=data_dict["title"],
                description=data_dict["description"],
                completed_at=data_dict["completed_at"]
                )
            return new_obj


    def check_complete_or_not(self):
        if self.completed_at:
            is_complete = True
        else:
            is_complete = False
        return is_complete
    

