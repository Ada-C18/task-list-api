from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"ERROR":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"ERROR":f"No {cls.__name__} with ID {model_id} in database"}, 404))

    return model