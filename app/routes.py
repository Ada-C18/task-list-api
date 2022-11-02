from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")

def validate_id_input(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"id {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"book {task_id} not found"}, 404))

    return task

@task_bp.route("",methods=["GET"])
def get_all_task():
    tasks_response = []
    tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "description": task.description,
                "completed_at": task.completed_at
            }
        )
    
    return make_response(jsonify(tasks_response), 200)

@task_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
    )

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.is_complete
            }
            }

    return jsonify(response_body), 201