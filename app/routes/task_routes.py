from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.title} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.title} {model_id} not found"}, 404))
    
    return model

def check_for_missing_data(request_body):
    required_values = ["title", "description", "completed_at"]
    for item in required_values:
        if item not in request_body:
            return False
    return True

@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not check_for_missing_data(request_body):
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)

@bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    task_query = Task.query

    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())
    
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()

    all_tasks = [task.to_dict() for task in tasks]

    return jsonify(all_tasks)

@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    one_task = validate_model(Task, task_id)
    return make_response({"task": one_task.to_dict()}, 200)

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    try:
        task.completed_at = request_body["completed_at"]
    except:
        pass

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({'details': f'Task {task_id} "{task.title}" successfully deleted'}, 200)