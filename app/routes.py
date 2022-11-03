from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    new_task = Task( 
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit()

    response_body = new_task.to_dict()

    return jsonify(response_body), 201


@task_bp.route('', methods=['GET'])
def get_all_tasks():
    tasks = Task.query.all()
    title_query_value = request.args.get("title") #not sure if this is good
    if title_query_value is not None:
        tasks = Task.query.filter_by(title=title_query_value)
    else:
        tasks = Task.query.all()

    result = []
    for item in tasks:
        result.append(item.to_dict())
    return jsonify(result), 200

# Get Tasks: No Saved Tasks
# As a client, I want to be able to make a GET request to /tasks when there are zero saved tasks and get this response:

# 200 OK
# []


@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify(chosen_task.to_dict()), 200




#helper function to get task by id:
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg":f"Invalid data type: {task_id}"}, 400))
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find task item with id: {task_id}"}, 404))
    return chosen_task