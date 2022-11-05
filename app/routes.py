from flask import Blueprint,jsonify, abort, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`.Id must be an integer."
        abort(make_response(jsonify({'message':response_str}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task: 
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({'message':response_str}), 404))
    return matching_task


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        )

    db.session.add(new_task)

    db.session.commit()

    return {
        "task":{
            "id" : new_task.id,
            "title" : new_task.title,
            "description" : new_task.description,
            "is_complete" : new_task.is_complete
        }
    }, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    
    tasks_query = request.args.get("title")
    if tasks_query is None:
        tasks = Task.query.all()

    else:
        tasks = Task.query.filter_by(title=tasks_query)

    response = []
    for task in tasks:
        task_dict = {
            "id":task.id,
            "title":task.title,
            "description":task.description,
            "is_complete":task.is_complete
        }
        response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    task_dict = {
        "task":{
            "id" : chosen_task.id,
            "title" : chosen_task.title,
            "description" : chosen_task.description,
            "is_complete" : chosen_task.is_complete
        }
    }
        
    return jsonify(task_dict), 200