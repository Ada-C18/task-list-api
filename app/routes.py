from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():   
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"task":new_task.to_dict()}), 201
    
    except KeyError :
        return jsonify({"details":"Invalid data"}), 400

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    rating_query_value = request.args.get("title")

    if rating_query_value is not None:
        tasks = Task.query.filter_by(rating=rating_query_value)
    else:
        tasks = Task.query.all()
    
    result = []

    for item in tasks:
        result.append(item.to_dict())
    
    return jsonify(result), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200

#helper function
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"details":"Invalid data"}, 400))
    
    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find Task with id:{task_id}"}, 404))
    return chosen_task

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    update_task = get_task_from_id(task_id)
    request_body = request.get_json()

    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        return jsonify({"msg": "Missing required data"}), 400
    
    db.session.commit()

    return jsonify({"task":update_task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details":f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'})