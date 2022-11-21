from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80)) 
    task_rel = db.relationship("Task", back_populates="task",lazy='True')
    task_id = db.Column(db.Integer, db.ForeignKey('task.id')) 

    def goal_dict(self):
            return {
                "id": self.goal_id,
                "title": self.title}
    
    @classmethod
    def from_dict(cls, book_data):
        new_Goal = Goal(title=book_data["title"])
        return new_Goal