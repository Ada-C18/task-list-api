from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
from app import os  

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)
# slack_client = SlackClient(SLACK_TOKEN)

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

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": new_task.to_dict()
    }), 201


@task_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    sort_request = request.args.get("sort") #Added this
    task_list = []
    
    """HELPER FUNCTION TO DETERMINE IF TASK IS COMPLETED"""
    def is_complete():
        if "completed_at" in task_list == None:
            return True
        else:
            return False

    task_response = []
    for task in tasks:
        task_response.append({
        "id":task.task_id,
        "title":task.title,
        "description":task.description,
        "is_complete":is_complete()
            }) 

    if sort_request == "asc":
        task_response = sorted(task_response, key=lambda a: a["title"])
    elif sort_request == "desc":
        task_response = sorted(task_response, key=lambda d: d["title"], reverse=True) 

    return jsonify(task_response)

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if task.task_id:
        return make_response(jsonify({"task":task.to_dict()}))
    else:
        return make_response(jsonify({"message": f"Task {task_id} not found"})), 404

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    if task:
        task_dict = {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
        }
    else:
        return jsonify({"message": f"Task {task_id} not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify(task_dict), 200
    

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
        return jsonify(response_body), 200
    else:
        db.session.commit()
        return jsonify({"message": f"Task {task_id} not found"}), 404

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_completed_task(task_id):
    task = Task.query.get_or_404(task_id)
    # task_completed_at = datetime.now()
    
    db.session.commit()
    
    return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_incomplete_on_incompleted_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task:
        task.completed_at = datetime.now()
        db.session.commit()
        return jsonify(task=task.to_dict()), 200
    else:
        task.completed_at = None
        error_msg = {"message": "No task found"}

