from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@bp.route("", methods=["POST"])
def create_a_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({
            "task": Task.to_dict(new_task)})), 201
