from flask import Blueprint, jsonify, abort, request, make_response
from app import db
from app.models.task import Task
from sqlalchemy import desc

task_bp= Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    
    selected_task = Task.query.get(id)
    print(selected_task)

    if not selected_task:
        abort(make_response({"details": "Task Not Found"}, 404))

    return selected_task

@task_bp.route("",methods=["GET"])
def get_all_tasks():
    sort_query= request.args.get("sort")
    
    if sort_query:
        if sort_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        else:
            tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()

    all_tasks = []
    for task in tasks:
        all_tasks.append({
            "id": task.task_id,
            "title" : task.title,
            "description": task.description, 
            "is_complete": task.is_complete
        })
    return jsonify(all_tasks), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    task = validate_task(task_id)

    return jsonify({"task": {
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete}}), 200

@task_bp.route("<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description= request_body["description"]
    
    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete}}), 200

@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    
    try:
        task = Task(
            title=request_body["title"],
            description=request_body["description"]
            )
    except:
        abort(make_response({"details":"Invalid data"},400))

    db.session.add(task)
    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id, 
        "title": task.title,
        "description": task.description,
        "is_complete": task.is_complete}}), 201

@task_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task=validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

