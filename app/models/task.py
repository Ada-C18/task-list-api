from app import db
import os


class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, default = None)
    #we want to make a column that is aboolean, 
    #and define that column to be True when there is a time stamp
    #and False when there is not a time stamp for completed.
    #for now I could make it be false no matter what ??
    is_complete = db.Column(db.Boolean, default = False)
    #old tries:
    #is_complete = db.column_property(os.path.exists(self.completed_at))
    
    # if completed_at == None:
    #     is_complete = False
    # else:
    #     is_complete = True

    def make_dict(self):
        """given a task, return a dictionary
        with all the attibutes of that task."""
        task_dict = {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            #I'm putting 'is_complete' to match test wave 1
            "is_complete": self.is_complete
        }
        return task_dict

    @classmethod
    def from_dict(cls, data_dict):
        #make the following a helper function:
        if "completed_at" in data_dict:
            completed_at = data_dict["completed_at"]
            if not completed_at:
                is_complete = False
            else:
                is_complete = True
        else: is_complete = False
        #end helper function.

        new_object = cls(
            title = data_dict["title"],
            description = data_dict["description"],
            is_complete = is_complete)
        return new_object
