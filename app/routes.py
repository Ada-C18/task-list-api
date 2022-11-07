from flask import Blueprint
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from app import db

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

def validate_request(data):
    try:
        new_task = Task(title =data["title"],
                description =data["description"])
    except:
        abort(make_response(
            {"details": "Invalid data"}, 400))
    return new_task


@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = validate_request(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({
            "task": {
            "id":new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}
    , 201)

@bp.route("", methods=["GET"])
def read_all_tasks():

    tasks = Task.query.all()

    get_response = []
    for task in tasks:
        get_response.append(dict(
            id=task.task_id,
            title=task.title,
            description=task.description,
            is_complete=bool(task.completed_at)
        ))
        
    return jsonify(get_response)

@bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_model(Task,task_id)


    get_response ={
        f"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete":  bool(task.completed_at)
        }}

    return get_response, 200

    
    

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    update_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return make_response(update_response), 200

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    task_response =  {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }
    return make_response(task_response), 200

