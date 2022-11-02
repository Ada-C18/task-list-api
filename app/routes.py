from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task= Task(title=request_body['title'],
                description=request_body['description'],
                completed_at=request_body['completed_at'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg":f"Successfully created Task with id={new_task.task_id}"}), 201


@task_bp.route('', methods=['GET'])
def get_all_tasks():
    #rating_query_value = request.args.get("rating")
    #if rating_query_value is not None:
    #    tasks = Task.query.filter_by(rating=rating_query_value)
    #else:
    tasks = Task.query.all()
    result = []
    for item in tasks:
        result.append(item.to_dict())  
    return jsonify(result), 200

@task_bp.route('/<task_id>', methods=['GET'])
def get_one_breakfast(task_id):
    chosen_task = get_task_from_id(task_id)

    return jsonify(chosen_task.to_dict()), 200

@task_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    update_task = get_task_from_id(task_id)
    request_body = request.get_json()

    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
        update_task.completed_at = request_body["completed_at"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400
    
    db.session.commit()
    return jsonify({"msg": f"Successfully updated task with id {update_task.task_id}"}), 200

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return jsonify({"msg": f"Successfully deleted task with id {task_to_delete.task_id}"}), 200

# helper
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data type: {task_id}"}, 400))

    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find task with id: {task_id}"}, 404))  
    return chosen_task
