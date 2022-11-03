from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

#route functions
@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at= request_body["completed_at"]
                    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("/tasks/1", methods=["DELETE"])
def delete_tasks():
    request_body = request.get_json()

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"}), 200
