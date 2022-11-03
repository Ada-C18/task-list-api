from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

#make a blueprint
task_bp = Blueprint("task_bp", __name__, url_prefix = "/tasks")

#constants: (refactor to make this from the database later.)
COL_NAMES = ["title", "description", "is_complete"] #later, add completed ad
COL_DEFAULTS = [None, "", False]
COL_NAME_DEFAULT_DICT = dict(zip(COL_NAMES, COL_DEFAULTS))

@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        task_dict = task.make_dict()
        response.append(task_dict)
    return jsonify(response), 200


@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    task_dict = task.make_dict()
    return make_response({"task": task_dict}, 200)
    
@task_bp.route("", methods = ["POST"])
def post_new_task():
    request_body = request.get_json()
    dict_of_field_vals = fill_empties_with_defaults(request_body)
    new_task = make_new_task(dict_of_field_vals)
    db.session.add(new_task)
    db.session.commit()
    task_dict = new_task.make_dict()
    response = {"task": task_dict}
    return make_response(response, 201)
    
    

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Task {task_id} must be an integer"
        abort(make_response({"message": response_str}, 400))
    task = Task.query.get(task_id)
    if not task:
        response_str = f"Task {task_id} not found"
        abort(make_response({"message": response_str}, 404))
    return task

def make_new_task(task_dict):
    new_task = Task(
        title = task_dict["title"],
        description = task_dict["description"],
        is_complete = task_dict["is_complete"]
    )
    return new_task

def fill_empties_with_defaults(request_body):
    """Go through entered fields.  
    If it has an entry, use that, if not, use the default."""
    task_dict = {}
    for field, default in COL_NAME_DEFAULT_DICT.items():

        if field not in request_body:
            task_dict[field] = default
        else:
            task_dict[field] = request_body[field]

    return task_dict
