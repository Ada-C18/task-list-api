from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    # checks input for all required fields
    if (("title") not in request_body
        or ("description") not in request_body):
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    task_response = Task.query.get(1)
    return make_response(task_response.to_dict(), 201)