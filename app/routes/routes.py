import json
from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

# create instance of blueprint class
tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# Wave 1 - Create a Task
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )

    # add to dict
    db.session.add(new_task)
    # submit changes
    db.session.commit()

    return jsonify(f"Task: {new_task}"), 201
    # return make_response(jsonify(new_task, 201))
    # return make_response(f"Book {new_book.title} successfully created", 201)


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at
            }
        )
    return jsonify(tasks_response)
