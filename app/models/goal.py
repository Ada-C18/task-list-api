from app import db


class Goal(db.Model):
    goal_id = db.Column(
        db.Integer, 
        primary_key=True)

    title = db.Column(db.String)
    tasks = db.relationship(
        "Task", 
        back_populates = 'goal', lazy = True)
    
    def to_dict(self):
        return {
            "id": self.goal_id,
            "title": self.title,
            #"tasks": self.tasks
        }
    
    def to_dict_incl_tasks(self):
        tasks = self.get_task_items()

        return {
            "id": self.goal_id,
            "title": self.title,
            "tasks": tasks
        }
    
    #Helper method to use in to_dict_incl_tasks()
    def get_task_items(self):
        if self.tasks is None:
            return None
        list_of_tasks = [item.to_dict_incl_goal_id() for item in self.tasks]
        return list_of_tasks

    @classmethod
    def from_dict(cls, dict):
        return cls (
            title = dict["title"],
        ) if len(dict) == 1 else cls (
            title = dict["title"],
            description = dict["description"],
            tasks = dict["tasks"]
        )
