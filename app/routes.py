from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    '''
    POST method - allows client to post tasks to the tasks record
    '''
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except:
        return make_response({"details": "Invalid data"}, 400)
    
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)


def validate_model(cls, model_id):
    '''
    helper function - throws an error code for an invalid ID
    '''
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify({"msg": f"{cls.__name__} with ID: {model_id} is invalid"}), 400))
    
    task = Task.query.get(model_id)

    if not task:
        abort(make_response(jsonify({"msg": f"{cls.__name__} with ID: {model_id} is not found"}), 404))
    return task


@tasks_bp.route("", methods=["GET"])
def view_all_tasks():
    '''
    GET method - allows client to view all tasks
    allows client to sort tasks alphabetically by title, in ascending and descending order
    '''
    sorted_query = request.args.get("sort")
    if sorted_query:
        if sorted_query == "asc":
            all_tasks = Task.query.order_by(Task.title.asc()).all()
        
        elif sorted_query == "desc":
            all_tasks = Task.query.order_by(Task.title.desc()).all()

    else:
        all_tasks = Task.query.all()

    request_body = []
    for task in all_tasks:
        request_body.append(task.to_dict())

    return jsonify(request_body), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def view_one_task(task_id):
    '''
    GET method - allows client to view one task by ID
    '''
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    '''
    PUT method - allows user to update one task record
    '''
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    '''
    DELETE method - allows user to remove specified task record
    '''
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}


#### is_complete endpoints ####
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    '''
    PATCH method - allows client to update task is_complete
    '''
    task = validate_model(Task, task_id)

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    '''
    PATCH method - allows client to mark completed task as incompmplete
    '''
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}
