from app import db

#Wave 1: CRUD for One Model

class Task(db.Model):

    id = db.Column(db.Integer, 
        primary_key=True, 
        autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, 
        nullable = True,
        default = None)
    goal_id = db.Column(
        db.Integer,
        db.ForeignKey("goal.goal_id"))
    goal = db.relationship(
        "Goal", 
        back_populates='task_items')
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": False if self.completed_at is None else True
        }
    # Source: 
    # https://stackoverflow.com/questions/52325025/use-of-if-else-inside-a-dict-to-set-a-value-to-key-using-python

    @classmethod
    def from_dict(cls, dict):
        return cls (
            title = dict["title"],
            description = dict["description"]
        ) if len(dict) == 2 else cls (
            title = dict["title"],
            description = dict["description"],
            completed_at = dict["completed_at"]
        )




        





