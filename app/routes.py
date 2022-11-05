from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

#Creating Task Blueprint (instantiating new Blueprint instance)
#use it to group routes(endpoints) that start with /tasks
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#Creating helper function validate_task to handle errors foe get a task by id
# Checks for valid data type (int)
# Checks that id provided exists in records
@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"task {new_task.title} successfully created", 201)


# Defining Endpoint
# Creating Route Function to Get all tasks


# Defining Endpoint
# Creating Route Function to Get one tasks

