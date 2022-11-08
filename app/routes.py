from flask import Blueprint,jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import date 

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`.Id must be an integer."
        abort(make_response(jsonify({'message':response_str}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task: 
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({'message':response_str}), 404))
    return matching_task


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"])

    db.session.add(new_task)

    db.session.commit()

    return {
        "task":{
            "id" : new_task.id,
            "title" : new_task.title,
            "description" : new_task.description,
            "is_complete" : new_task.is_complete
        }
    }, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("title")

    sort_param = request.args.get("sort")

    if not title_param:
        tasks = Task.query.all()
    
    if sort_param  == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()

    response = [task.to_dict() for task in tasks]
    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    task_dict = {
        "task":{
            "id" : chosen_task.id,
            "title" : chosen_task.title,
            "description" : chosen_task.description,
            "is_complete" : chosen_task.is_complete
        }
    }
        
    return jsonify(task_dict), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message": "request must include name, description, type "}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"] 

    db.session.commit()

    return {
        "task":{
            "id" : chosen_task.id,
            "title" : chosen_task.title,
            "description" : chosen_task.description,
            "is_complete" : chosen_task.is_complete
        }
    }, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)

    db.session.delete(chosen_task)

    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}), 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_is_complete(task_id):
    update_is_valid_id = get_one_task_or_abort(task_id)

    update_is_valid_id.complete_at = date.today()
    db.session.commit()

        
    return jsonify({"task":update_is_valid_id.to_dict()}), 200

# @task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
# def update_is_complete(task_id):
    
#     return jsonify({"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}), 200