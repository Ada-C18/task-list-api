from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    def create_dict(self):
            goal_as_dict = {}
            goal_as_dict["id"] = self.goal_id  
            goal_as_dict["title"] = self.title
            
            return goal_as_dict

    def update(self,req_body):
        self.title = req_body["title"]

    @classmethod 
    def new_instance_from_dict(cls, req_body):
        new_dict = cls(
                        title = req_body["title"],
                        )
        return new_dict

