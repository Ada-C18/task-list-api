from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return make_response(jsonify({
            "details": "Invalid data"
        }), 400)

    db.session.add(new_task)
    db.session.commit()

    task_response = {
        "task": new_task.to_dict()
    }

    return make_response(jsonify(task_response), 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")
    limit_query = request.args.get("limit")
    
    task_query = Task.query

    if title_query:
        tasks = task_query.filter_by(title=title_query)
    
    if description_query:
        tasks = task_query.filter_by(description=description_query)
    
    if completed_at_query:
        tasks = task_query.filter_by(completed_at=completed_at_query)

    if limit_query:
        tasks = task_query.limit(limit_query)

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task_response = {
        "task": task.to_dict()
    }

    return make_response(jsonify(task_response), 200)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    task_response = {
        "task": task.to_dict()
    }

    return make_response(jsonify(task_response), 200)

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    # validate, commit, make response
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    task_response = {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }

    return make_response(jsonify(task_response), 200)

