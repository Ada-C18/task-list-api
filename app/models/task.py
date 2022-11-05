from app import db


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    @classmethod
    def from_dict(cls, response_dict):
        return cls(
            title=response_dict["title"],
            description=response_dict["description"],
            completed_at=response_dict["completed_at"]
        )

    # @classmethod
    # def response_dict(cls, data_dict):
    #     return cls(
    #     id=self.task_id,
    #     title=data_dict["title"],
    #     description=data_dict["description"],
    #     is_complete=data_dict["completed_at"],
    #     )

    def to_dict(self):
        return_dict = {
            "task": {  # how to separate this out?
                "id": self.task_id,
                "title": self.title,
                "description": self.description,
                "is_complete": self.completed_at
            }}  # how to get T/F here?
        return return_dict

    def resp_all_dict(self):
        return_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at
        }  # how to get T/F here?
        return return_dict
