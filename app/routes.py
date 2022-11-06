from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

#Creating Task Blueprint (instantiating new Blueprint instance)
#use it to group routes(endpoints) that start with /tasks
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")



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



# Defining Endpoint and Creating Route Function to GET(read) All Tasks
# Task.query.all() is SQLAlchemy is syntax tells Task to query for all() tasks. This method returns a list of instances of task
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append( 
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        )
    return jsonify(tasks_response)

#Creating helper function validate_task to handle errors foe get a task by id
# Checks for valid data type (int)
# Checks that id provided exists in records
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

# Defining Endpoint and Creating Route Function to GET(read) One Task
#Refactored to define task as return value of helper function validate_task
    #task = Task.query.get(task_id) how task is defined without helper function
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        }

# Defining Endpoint and Creating Route Function to UPDATE a Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        }

# Defining Endpoint and Creating Route Function to UPDATE a Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    }
