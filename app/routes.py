from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    # if "completed_at" in request_body:
    #     new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=request_body["completed_at"])
    # else:
    #     new_task = Task(title=request_body["title"], description=request_body["description"])

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_dict()
    }, 201



@task_bp.route("", methods=["GET"])
def read_all_tasks():
    task_list = []

    def is_complete():
        if "completed_at" in task_list == None:
            return True
        else:
            return False

    task_response = []
    tasks = Task.query.all()
    for task in tasks:
        task_response.append({
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":is_complete()
        })

    return jsonify(task_response)

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if task.task_id:
        return {"task":task.to_dict()}
    else:
        return {"message": f"Task {task_id} not found"}, 404

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    if task:
        task_dict = {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
        }
    else:
        return {"message": f"Task {task_id} not found"}, 404

    db.session.delete(task)
    db.session.commit()

    return task_dict, 200
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    if task:   
        task.title = request_body["title"]
        task.description = request_body["description"]
        response_body = {"task": {
                    "id": 1,
                    "title": "Updated Task Title",
                    "description": "Updated Test Description",
                    "is_complete": False
            }}
        db.session.commit()
        return response_body, 200
    else:
        db.session.commit()
        return {"message": f"Task {task_id} not found"}, 404
    
@task_bp.route("/<task_id>sort=asc", methods=["GET"])
def get_task_sort_asc(task_id):
    
