from flask import Blueprint
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__,url_prefix="/tasks")


# Helper function
def get_task_from_id():
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {task_id}"}, 200))

    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find the task with id: {task_id}"}, 404))
    
    return chosen_task


@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    new_task= Task(title=request_body["title"],
                description=request_body["description"]
                # completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

@tasks_bp.route('', methods=['GET'])
def get_all_planets():
    name_query_value = request.args.get('name')
    if name_query_value is not None:
        tasks = Task.query.filter_by(name=name_query_value)
    else:
        tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append(task.to_dict())
    
    return jsonify(result), 200


