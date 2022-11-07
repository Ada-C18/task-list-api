from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.name} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"message": f"{cls.name} {model_id} not found"}, 404))

@bp.route("", methods=["GET"])
def read_all_tasks():
    all_tasks = []
    tasks = Task.query.all()
    for task in tasks:
        all_tasks.append(task.to_dict())
    return jsonify(all_tasks)
