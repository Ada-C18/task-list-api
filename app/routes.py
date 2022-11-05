from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


# def get_one_task_or_error(task_id):
#     try:
#         task_id = int(task_id)
#     except ValueError:
#         response_body = "Invalid data"
#         return make_response(jsonify({"details": response_body}), 400)

#     task_found = Task.query.get(task_id)

#     if task_found is None:
#         response_body = "Task id not found"
#         return make_response(jsonify({"details": response_body}), 404)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("", methods=["POST"])
def add_task():

    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = None
    )

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
            }
        }

    return jsonify(response), 201 # is this giving me the output needed?

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks = Task.query.all()

    response = []

    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False # will need help figuring out how to use this
        }
        response.append(task_dict)

    return jsonify(response), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = Task.query.get(task_id)

    if task:
        response_dict = {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
                }
            }
        return jsonify(response_dict), 200

    if task is None:
        response_body = "Whoopsie daisy! Task id is lost and was not found"
        return jsonify(response_body), 404

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_title_and_description(task_id):

    task_to_update = Task.query.get(task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

# this will need to be replaced with the updated instances
    response_body = {       
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
            }
        }
    # this is what the response body should look like after updating the data
    # response_body = {       
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": False
    #         }
    #     }
    return jsonify(response_body), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_data_from_db(task_id):

    task_to_delete = Task.query.get(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    response_body = "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
    return jsonify({"details": response_body}), 200