from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")

# def validate_id_input(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"message":f"id {task_id} invalid"}, 400))

#     task = Task.query.get(task_id)

#     if not task:
#         abort(make_response({"message":f"book {task_id} not found"}, 404))

#     return task

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = f"Invalid task_id {task_id}. ID must be an integer."
        return jsonify({"message": response}), 400

    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Task with id {task_id} was not found in the database."

        abort(make_response({"message": response_str}, 404))
    
    return matching_task

@task_bp.route("",methods=["GET"])
def get_all_tasks():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete
            }
        )

    return make_response(jsonify(tasks_response), 200)

@task_bp.route("/<task_id>",methods=["GET"])
def get_task_by_id(task_id):
    task_with_id = get_one_task_or_abort(task_id)

    response_body = {
        "task": {
            "id": task_with_id.task_id,
            "title": task_with_id.title,
            "description": task_with_id.description,
            "is_complete": task_with_id.is_complete
        }}

    return jsonify(response_body), 200
    

@task_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
    )

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
            }
            }

    return jsonify(response_body), 201

@task_bp.route("/<task_id>",methods=["PUT"])
def update_task(task_id):
    selected_task = get_one_task_or_abort(task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"message": "Request must include title and description"})
    
    selected_task.title = request_body["title"]
    selected_task.description = request_body["description"]

    db.session.commit()

    response_body = {
        "task": {
                "id": selected_task.task_id,
                "title": selected_task.title,
                "description": selected_task.description,
                "is_complete": selected_task.is_complete
                }}
    
    return jsonify(response_body), 200