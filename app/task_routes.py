from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_by")

    task_query = Task.query

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    
    if description_query:
        tasks = Task.query.filter_by(description=description_query)
    
    if completed_at_query:
        tasks = Task.query.filter_by(completed_by=completed_at_query)

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)