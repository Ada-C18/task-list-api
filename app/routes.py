from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_tasks(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details":f"{task_id} invalid data"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))
    
    return task 



@tasks_bp.route("", methods=["POST"])
def create_tasks():
    title = request.json.get("title", None)
    description = request.json.get("description")
    if not title or not description:
        return jsonify({"details": "Invalid data"}), 400

        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
            )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def get_tasks():
    task_param = request.args.get("sort")

    if task_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif task_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    else:
        tasks = Task.query.all()
    request_body = []
    result_list = [task.to_dict() for task in tasks]

    return jsonify(result_list), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_tasks(task_id)

    return jsonify(task.one_task_in_dict()), 200
    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def put_one_task(task_id):
    task = validate_tasks(task_id)
    request_body = request.get_json()

    task.one_saved_task(request_body)

    db.session.commit()

    return jsonify(task.one_task_in_dict()), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_tasks(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task# {task_id} successfully deleted"), 200
