from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from .models.task import Task

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def validate_task_dict(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False) and request_body.get("description", False)):
        abort(make_response({'details': 'Invalid data'}, 400))
    # if request_body.get("copmleted_at", 1) == 1:
    #     abort(make_response({'details': 'Invalid data'}, 400))

@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    validate_task_dict(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    

    return make_response({"task": new_task.to_dict()}, 201)

@bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    limit_query = request.args.get("limit")

    task_query = Task.query

    if title_query:
        cat_query = cat_query.filter_by(personality=title_query)

    if description_query:
        cat_query = cat_query.filter_by(color=description_query)

    if limit_query:
        cat_query = cat_query.limit(limit_query)

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

@bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)
    return make_response({"task": task.to_dict()}, 200)


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()
    # return make_response(f"Task #{task.id} successfully deleted"), 200
    return make_response({"details":f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)