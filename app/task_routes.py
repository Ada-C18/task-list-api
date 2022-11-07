from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

def validate_task(cls,task_id):
    try:
        task_id=int(task_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {task_id} invalid. Must be an integer"}, 400))
        
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"{cls.__name__} {task_id} not found"}, 404))

    return task


@task_bp.route("/", strict_slashes=False, methods =["GET"])
def read_all_task():

    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)


@task_bp.route("/<id>", strict_slashes=False, methods =["GET"])
def read_one_task(id):
    
    task = validate_task(Task,id)
    return {"task":task.to_dict()}, 200

@task_bp.route("", strict_slashes=False, methods =["POST"])
def create_task():

    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    except:

        return make_response(jsonify({"details": "Invalid data"}),400)

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()},201


@task_bp.route("/<id>", strict_slashes=False, methods =["PUT"])
def update_task(id):

    task = validate_task(Task,id)
    request_body = request.get_json()

    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        return make_response(jsonify({'warning':'Enter both title and description or use patch method'}),400)

    db.session.commit()
    return make_response(jsonify({"task":task.to_dict()}),200)


@task_bp.route("/<id>", strict_slashes=False, methods =["DELETE"])
def delete_task(id):

    task = validate_task(Task,id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f"{Task.__name__} {task.id} \"{task.title}\" successfully deleted"
    }

    return make_response(jsonify(response_body),200)
