from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(cls, task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message" : f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message" : f"task {task_id} not found"}, 404))

    return task


@bp.route("", methods=["POST"])
def create_a_task():
    try: 
        request_body = request.get_json()

        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify({
                "task": Task.to_dict(new_task)})), 201
    except:
        abort(make_response({"details": "Invalid data"}, 400))

@bp.route("", methods=["GET"])
def get_saved_tasks():
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(Task, task_id)
    return make_response(jsonify({
        "task": Task.to_dict(task)})), 200

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({
        "task": Task.to_dict(task)})), 200

@bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details" : f"Task {task_id} \"{task.title}\" successfully deleted"}))






