from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

#validate task
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

#create a task
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
            
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
    except KeyError:
        return make_response({
            "details": "Invalid data"
            }, 400)

    db.session.add(new_task)
    db.session.commit()


    return make_response({
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)}, 201)

#read all tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    
    task_sort_query = request.args.get("title")
    
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    if task_sort_query:
        return jsonify(tasks_response.sort())
    else:
        return jsonify(tasks_response)

#read one task
@tasks_bp.route("<task_id>", methods=["GET"])
def read_one_tasks(task_id):
    task = validate_task(task_id)
    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }}

#update one task
@tasks_bp.route("<task_id>", methods=["PUT"])
def update_one_tasks(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }}

#delete one task
@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    # return make_response(f"Task #{task.task_id} successfully deleted")
    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}



    

    
