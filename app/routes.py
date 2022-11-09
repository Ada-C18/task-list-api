from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from sqlalchemy import desc
from datetime import datetime

from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['GET'])
def get_all_tasks():
    #title_query_value = request.args.get("title") # has to be string
    sort_query_value = request.args.get("sort") # has to be string
    #if title_query_value is not None: # ! rather checking not None
    #    tasks = Task.query.filter_by(title=title_query_value)
    if sort_query_value == 'asc':
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query_value == 'desc':
        tasks = Task.query.order_by(desc(Task.title)).all()
    else:
        tasks = Task.query.all()


    result = []
    for item in tasks:
        result.append(item.to_dict())

    return jsonify(result), 200

@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_model_from_id(Task, task_id)
    return jsonify({"task": chosen_task.to_dict()}), 200

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@task_bp.route('/<task_id>', methods=['PUT'])
def update_one_task(task_id):
    update_task = get_model_from_id(Task, task_id)

    request_body = request.get_json()

    try:
        #update_task = Task.from_dict(request_body)
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400 

    db.session.commit()
    return jsonify({"task": update_task.to_dict()}), 200

@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_model_from_id(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'}), 200

@task_bp.route('/<task_id>/<mark_tf>', methods=['PATCH'])
def change_value_of_task(task_id, mark_tf):
    task_to_patch = get_model_from_id(Task, task_id)

    #request_body = request.get_json()

    try:
        if mark_tf == 'mark_complete':
            task_to_patch.is_complete = True # True or False
            task_to_patch.completed_at = datetime.utcnow()
        elif mark_tf == 'mark_incomplete':
            task_to_patch.is_complete = False # True or False
            task_to_patch.completed_at = None
        #task_to_patch.is_complete = request_body["is_complete"] # True or False
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400 

    db.session.commit()
    return jsonify({"task": task_to_patch.to_dict()}), 200


def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg": f"invalid data: {model_id}"}, 400))

    chosen_task = cls.query.get(model_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find task item with id: {model_id}"}, 404))

    return chosen_task