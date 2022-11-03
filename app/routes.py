from app import db
from app.models import task
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
#Create a Task: Valid Task With null completed_at
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    )
    db.session.add(new_task)
    db.session.commit()
    return make_response({"task":{
        "id":new_task.task_id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":False
    }},201)

@tasks_bp.route("", methods=["Get"])
def get_all_task():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title":task.title,
            "description":task.description,
            "is_complete":False
        })
    return make_response(jsonify(tasks_response),200)
#Get One Task: One Saved Task
def check_valid_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"invalid task id {task_id}"}, 400))
    
    task = Task.query.get(task_id)
    if not task:
        return abort(make_response({"message": f"No id {task_id} task"}, 404))
    return task
    
@tasks_bp.route('/<task_id>', methods =["GET"])
def get_task_by_id(task_id):
    task = check_valid_id(task_id)
    return make_response({"task":{
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":False
    }}, 200)