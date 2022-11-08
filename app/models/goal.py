from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    tasks = db.relationship("Task", back_populates="goal",lazy=True)    
    
    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title
            # "tasks": self.get_task_list()                        
        }

    @classmethod
    def from_dict(cls,goal_dict):
        return cls(
            title=goal_dict["title"]
                        
        )
    
    def get_task_list(self):
        list_of_tasks = []
        for item in self.tasks:
            list_of_tasks.append(item.to_dict())
        return list_of_tasks