from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc #(used in read_all_tasks for sorting)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#CREATE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("", methods=["POST"])
def create_task():
        request_body = request.get_json()
        try:
            new_task = Task.from_dict(request_body)
        except KeyError:
            return jsonify ({"details": "Invalid data"}), 400
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": new_task.to_dict()}), 201

#READ Routes (Wave 1: CRUD routes)
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    #(Wave 2: Query param: sort)
    if "sort"in request.args or "SORT" in request.args:
        sort_query_val = request.args.get("sort") if "sort"in request.args else \
            request.args.get("SORT") 
        if sort_query_val.lower() == "asc":
            tasks = Task.query.order_by(Task.title).all()
        elif sort_query_val.lower() == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all() 
            # Source: https://stackoverflow.com/questions/4186062/sqlalchemy-order-by-descending
        else:
            return jsonify({"msg": f"Invalid query value: {sort_query_val}"}), 400
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response), 200

@tasks_bp.route("<task_id>", methods=["GET"])
def read_task_by_id(task_id): 
    task = validate_task(task_id)
    return jsonify({"task":task.to_dict()}), 200

#Helper function for use in READ route: read_task_by_id and UPDATE route: update_task
def validate_task(id):
    try:
        task_id = int(id)
    except:
        abort(make_response(jsonify({"msg":f"invalid id: {id}"}), 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response(jsonify({"msg": f"No task found with given id: {id}"}), 404))

    return task

#UPDATE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    if len(request_body) > 2 and request_body["completed_at"]:
        task.completed_at = request_body["completed_at"]
    db.session.commit()

    return jsonify({"task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False if task.completed_at is None else True
        }}), 200

# DELETE Routes (Wave 1: CRUD Routes)
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_route(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200

