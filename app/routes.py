from flask import Blueprint, jsonify, abort, make_response, request
from os import abort
from app.models.task import Task
from app import db
import json
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

now = datetime.now() 
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

@tasks_bp.route("", methods=['POST'])
def created_task():
    request_body = request.get_json()
    print(request_body)
    created_task = Task(title=request_body["title"],
                description=request_body["description"],
            completed_at=request_body["completed_at"])
    
    if created_task.title == "":
        return f"{created_task.title}, 400 Bad Request"

    else:
        db.session.add(created_task)
        db.session.commit()

        return jsonify({"task": created_task.build_task_dict()}), 201


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route('', methods=['GET'])
def query_all():
    all_tasks = Task.query.all()
    tasks_lists = []
    for task in all_tasks:
            tasks_lists.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "completed_at": bool(task.completed_at)
            })
    print(tasks_lists)
    return jsonify(tasks_lists)

@tasks_bp.route('/<task_id>', methods=['GET'])
def one_saved_task(task_id):
    # task_validate = validate_task_id(task_id)
    task = Task.query.get(task_id)
    if task == None:
        return "The task ID submitted, does not exist: error code 404"
    else:      
        return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description
        }
    #
    # print(task)

@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_tasks(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(f"Task {task_id} successfully updated", 200)

@tasks_bp.route('/<id>', methods=['DELETE'])
def delete_tasks(task_id):
    test = validate_task_id(task_id)

    db.session.delete(test)
    db.session.commit()

    return make_response(f"Test #{test.id} successfully deleted, 200 OK")



# # ### Create a Task: Invalid Task With Missing Data

# # #### Missing `title`

# # As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

# # ```json
# # {
# #   "description": "Test Description",
# #   "completed_at": null
# # }
# # ```

# # and get this response:

# # `400 Bad Request`

# # ```json
# # {
# #   "details": "Invalid data"
# # }
# # ```

# # so that I know I did not create a Task that is saved in the database.

# # #### Missing `description` 
# # If the HTTP request is missing `description`, we should also get this response:
# # `400 Bad Request`

# # ```json
# # {
# #   "details": "Invalid data"
# # }
# # ```
# @tasks_bp.route('/', methods=['DELETE'])
# def missing_description():
#     pass 


# #### Missing `completed_at`
# # If the HTTP request is missing `completed_at`, we should also get this response:
# # `400 Bad Request`
# # ```json0️⃣
# # {
# #   "details": "Invalid data"
# # }
# # ```

