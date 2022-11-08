from app import db
from app.models.task import Task
from flask import Blueprint,jsonify, make_response, request, abort
import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id= int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}))
    
    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

def validate_dict(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False) and request_body.get("description", False)):
        abort(make_response({"details": "Invalid data"},400))
    return request_body

@task_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()
    task_dict = validate_dict(request_body)
    new_task = Task.from_dict(task_dict)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }), 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_task_query = request.args.get("sort")
    task_query = Task.query
    if sort_task_query:
        if sort_task_query == "asc":
            task_query = task_query.order_by(Task.title)
        else:
            task_query = task_query.order_by(Task.title.desc())
    tasks = task_query.all()
    
    tasks_response =[]
    
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response)

@task_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)
    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }}
    return make_response(jsonify(response_body), 200)
    
@task_bp.route("/<id>",methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }), 200)

@task_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {id} "{task.title}" successfully deleted'}),200
@task_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_model(Task,id)

    request_body = request.get_json()

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    return make_response(jsonify(task.to_dict()), 200)

@task_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify(task.to_dict()), 200)










