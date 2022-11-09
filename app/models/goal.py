from app import db


class Goal(db.Model):
    goal_id = db.Column(
        db.Integer, 
        primary_key=True)

    title = db.Column(db.String)
    task_items = db.relationship(
        "Task", 
        back_populates = 'goal')
    
    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            #"task_items": self.task_items
        }

    def get_task_items(self):
        list_of_tasks = [item.to_dict() for item in self.task_items]
        
    @classmethod
    def from_dict(cls, dict):
        return cls (
            title = dict["title"],
        ) if len(dict) == 1 else cls (
            title = dict["title"],
            description = dict["description"],
            task_items = dict["task_items"]
        )
