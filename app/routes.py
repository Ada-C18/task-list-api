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
#       CREATE RESOURCE
#==============================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.new_instance_from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.from_dict(), 201)
