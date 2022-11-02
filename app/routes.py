from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id, action):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"Could not {action} {cls.__name__} \'{model_id}\' as it is invalid"}, 400))

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"Could not {action} {cls.__name__} {model_id} as it was not found"}, 404))
    
    return model

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id, "get")
    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def post_a_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("/<task_id>", methods=["PUT","PATCH"])
def update_one_task(task_id):
    task_to_update = validate_model(Task, task_id, "update")
    request_body = request.get_json()

    if request_body["title"]:
        task_to_update.title = request_body["title"]
    if request_body["description"]:
        task_to_update.description = request_body["description"]

    db.session.commit()
    return jsonify({"task": task_to_update.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_model(Task, task_id, "delete")

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f"Task {task_to_delete.task_id} \"{task_to_delete.title}\" successfully deleted"}), 200
