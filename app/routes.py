from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid Data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details": "Invalid Data"}, 404))

    return model


@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(dict(task = task.to_dict()), 200)


@bp.route("", methods=["GET"])
def read_all_planets():

    sort_query = request.args.get('sort')

    tasks = Task.query

    if sort_query == 'asc':
        tasks = tasks.order_by(Task.title.asc())

    if sort_query == 'desc':
        tasks = tasks.order_by(Task.title.desc())

    tasks = tasks.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        request_body["title"] and request_body["description"]
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    try:
        request_body["completed_at"]
    except:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    else:
        new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(dict( task = new_task.to_dict()), 201)

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    try:
        request_body["completed_at"]
    except:
        task.title = request_body["title"]
        task.description = request_body["description"]

    else:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

    db.session.commit()
    return make_response(dict(task = task.to_dict()), 200)

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()  
    return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

# @bp.route("/<task_id>", methods=["PATCH"])
# def delete_task(task_id):
#     task = validate_model(Task, task_id)


#     db.session.commit()  
#     return make_response(dict(task = task.to_dict()), 200)