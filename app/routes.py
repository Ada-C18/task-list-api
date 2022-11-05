from app import db
from app.models.task import Task 
from flask import Blueprint, jsonify, abort, make_response, request
from collections import OrderedDict
from sqlalchemy import asc, desc
bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
        
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model 

@bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
    
        new_task = Task.from_dict(request_body)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()
    
    return make_response(jsonify({
            "task": Task.to_dict(new_task)})), 201

@bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")
    tasks_query = Task.query
    
    if sort_query== "asc":
        tasks_query = tasks_query.order_by(asc(Task.title))
    if sort_query == "desc":
        tasks_query = tasks_query.order_by(desc(Task.title))

    tasks = tasks_query.all()

    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response), 200

@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    result_task = validate_model(Task, task_id)
    return jsonify({
            "task": result_task.to_dict()}), 200

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({
            "task": task.to_dict()})), 200

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
    "details": f"Task {task_id} \"{task.title}\" successfully deleted"
}))