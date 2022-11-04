from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

#POST request
@tasks_bp.route("",methods = ['POST'])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body['title'],
                    description = request_body['description'],
                    completed_at = request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f'Task {new_task.title} has been successfully created.', 201))
