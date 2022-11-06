from app import db

class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True)





# def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "breed": self.breed,
#             "age": self.age,
#             "gender": self.gender
#         }