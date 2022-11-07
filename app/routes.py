from app import db
from flask import abort, Blueprint, jsonify, make_response, request
from .models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#==============================
#       HELPER FUNCTIONS
#==============================
def validate_id(id):
    try:
        id = int(id)
    except:
        abort(make_response(jsonify({"message":f"{id} invalid."}), 400))


#==============================
#         CREATE TASK
#==============================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.new_instance_from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(f'"task": {new_task.create_dict()}', 201)


#==============================
#        READ ALL TASKS
#==============================
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.create_dict() for task in tasks]

    return make_response(jsonify(tasks_response), 200)

