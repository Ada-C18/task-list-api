from app import db



class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship('Goal', back_populates='tasks')

    def to_dict(self):
        if self.completed_at is None:
            return {
                        # "task": {
                            "id": self.task_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": False
                        }
        return {
                        # "task": {
                            "id": self.task_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": True
                        }

#do I need to create a new funciton or incorporate "goal_id" into dict print out
    def to_dict_relationship(self):
        if self.completed_at is None:
            return {
                        # "task": {
                            "id": self.task_id,
                            "goal_id": self.goal_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": False
                        }
        return {
                        # "task": {
                            "id": self.task_id,
                            "goal_id": self.goal_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": True
                        }