from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.routes_helper import get_one_obj_or_abort

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()

    # new_task = Task.from_dict(request_body)
    if "title" not in response_body or\
       "description" not in response_body:
       # “is_complete” not in respnse_body
        return jsonify({"details": "Invalid data"}), 400
    new_task = Task(
        title = response_body["title"],
        description = response_body["description"],)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("sort") 

    if title_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    elif title_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    
    chosen_task = get_one_obj_or_abort(Task, task_id)

    return jsonify({
        "task": chosen_task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_with_new_vals(task_id):

    chosen_task = get_one_obj_or_abort(Task, task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message":"Request must include title, description"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]


    db.session.commit()

    return jsonify({f"task": chosen_task.to_dict()}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    db.session.delete(chosen_task)

    db.session.commit()

    return jsonify({"details": f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'}), 200
