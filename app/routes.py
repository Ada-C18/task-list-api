from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

#Creating Task Blueprint (instantiating new Blueprint instance)
#use it to group routes(endpoints) that start with /tasks
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Creating helper function validate_task to handle errors foe get a task by id
# Checks for valid data type (int)
# Checks that id provided exists in records


# Defining Endpoint and Creating Route Function to CREATE a task
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json() #This method "Pythonifies" the JSON HTTP request body by converting it to a Python dictionary
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        
        )

    #communicating to the db to collect and commit the changes made in this function
    #saying we want the database to add new_task
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
        }, 201



# Defining Endpoint
# Creating Route Function to Get one tasks

