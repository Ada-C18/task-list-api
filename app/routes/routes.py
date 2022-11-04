import json
from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import datetime

# create instance of blueprint class
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# error handling
def validate_task(task_id):
    # invalid task id
    try:
        task_id = int(task_id)
    except:
        abort(make_response({{"message": f"Invalid task id {task_id}."}}, 400))

    task = Task.query.get(task_id)

    # task not found
    if not task:
        abort(make_response({"message": f"Task {task_id} not found."}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or \
            "description" not in request_body:
        # or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    # completed_at_status = None
    # is_complete_status = None
    # if "completed_at" in request_body:
    #     is_complete_status = True
    #     # completed_at_status = DATETIME
    # else:
    #     is_complete_status = False
    #     completed_at_status = None

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=None,
        # completed_at=completed_at_status,
        # is_complete=is_complete_status,
    )

    # add to dict
    db.session.add(new_task)
    # submit changes
    db.session.commit()

    # TODO create method to convert response to json
    # task_dict = Task.to_dict(new_task)
    response = {
        "task": new_task.to_dict()
    }

    return response, 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # ADDING FUNCTIONALITY
    # functionality: sort task by title -> Add title query param
    order_param = request.args.get("sort")

    if order_param is None:
        tasks = Task.query.all()
    elif order_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif order_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    tasks_response = []
    for task in tasks:
        task_dict = task.to_dict()

        tasks_response.append(task_dict)

    return jsonify(tasks_response)


# Create GET route for 1 task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_bike(task_id):
    chosen_task = validate_task(task_id)
    # chosen_task = Task.query.get(task_id)

    # returns jsonified object and response code as tuple
    response = {
        "task": chosen_task.to_dict()
    }

    return response, 200


# Update Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    response = {
        "task": task.to_dict()
    }

    db.session.commit()

    return jsonify(response), 200
    # return response, 200 # jsonify needed here?
# REQUEST
# {
#   "title": "Updated Task Title",
#   "description": "Updated Test Description",
# }
# RESPONSE
# {
#   "task": {
#     "id": 1,
#     "title": "Updated Task Title",
#     "description": "Updated Test Description",
#     "is_complete": false
#   }
# }


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }

    return jsonify(response), 200

# RESPONSE
# {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# }

    # assert response_body == {
    #     "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    # }


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_to_complete(task_id):
    task = validate_task(task_id)

    # request_body = request.get_json()

    # if request_body["completed_at"] == True:
    # if task.completed_at is not None:
    # if "completed_at" in request_body:
    task.completed_at = datetime.utcnow()
    # else:
    #     # task.is_complete = False
    #     task.completed_at = None

    updated_task = task.to_dict()

    db.session.commit()

    response = {
        "task": updated_task
    }

    return response, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_to_incomplete(task_id):
    task = validate_task(task_id)

    # request_body = request.get_json()

    # if "completed_at" in request_body:
    # if request_body["is_complete"] == True:
    #     # updated_task["is_complete"] = True
    #     task.completed_at = datetime.utcnow()
    # else:
    #     # task.is_complete = False
    task.completed_at = None

    db.session.commit()

    updated_task = task.to_dict()
    response = {
        "task": updated_task
    }

    return response, 200

# PATCH response
# {
#   "task": {
#     "id": 1,
#     "title": "Go on my daily walk 🏞",
#     "description": "Notice something new every day",
#     "is_complete": true
#   }
# }
