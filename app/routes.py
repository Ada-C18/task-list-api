from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db
from sqlalchemy import asc
from datetime import datetime
from datetime import timezone



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id=int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
    model =  cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model

@task_bp.route("", methods = ["GET"])
def read_all_tasks():
    query_sort= request.args.get("sort")
    if query_sort:
        if query_sort == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        elif query_sort == "desc":
            tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_data=[task.to_dict() for task in tasks]
    return jsonify(tasks_data)

@task_bp.route("/<task_id>", methods = ["GET"])
def read_one_task(task_id):

    task = validate_model(Task, task_id)
    
    return {"task":task.to_dict()}

@task_bp.route("", methods = ["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_task)
    db.session.commit()
    return {"task":new_task.to_dict()}, 201

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}),200)

    #Sorting Query Params, Wave 2

# def order_by_title_asc(sort):
#     order = Task.query.order_by(Task.title).asc()
#     tasks_data=[task.to_dict() for task in order]
#     return jsonify(tasks_data)

# SELECT user.user_id AS user_user_id FROM user ORDER BY case when ifnull(nickname, '') = '' then 0 else 1 end desc LIMIT 1

# Wave 3 mark complete 
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_complete(task_id):

    task = validate_model(Task, task_id)
    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    return {"task":task.to_dict()}, 200
    


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task":task.to_dict()}, 200
    