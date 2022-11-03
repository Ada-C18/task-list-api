from flask import Blueprint
from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    '''
    POST method - allows client to post tasks to the tasks record
    '''
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.task_dictify()}

    return make_response(jsonify(response_body), 201)


@tasks_bp.route("", methods=["GET"])
def view_all_tasks():
    '''
    GET method - allows client to view all tasks
    '''
    tasks = Task.query.all()

    request_body = []
    for task in tasks:
        request_body.append(task.task_dictify())

    return jsonify(request_body), 200


def validate_task(task_id):
    '''
    helper function - throws an error code for an invalid ID
    '''
    try:
        task_id = int(task_id)
    except:
        abort(make_response(jsonify({"msg": f"task with {task_id} is invalid"}), 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"msg": f"task with {task_id} is not found"}), 404))
    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def view_one_task(task_id):
    '''
    GET method - allows client to view one task by ID
    '''
    task = validate_task(task_id)

    return task.task_dictify()