from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_complete = db.Column(db.Boolean, default=False)  
    # #one-to-many relationship where goal has-many tasks, and a task belongs to one goal
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'))
    goal = db.relationship("Goal", back_populates="tasks")
    # #db.relationship is a fx that adds on an attr to our Task model and returns the goal instance for that task