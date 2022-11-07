from app import db
from datetime import date
from app.models.task import Task
from app.models.goal import Goal
from app.routes.routes_helpers import *
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        task_query = Task.query

        sort = request.args.get("sort")
        if sort == "desc":
            task_query = task_query.order_by(Task.title.desc())
        elif sort == "asc":
            task_query = task_query.order_by(Task.title.asc())

        tasks = task_query.all()
        tasks_response = [task.to_json() for task in tasks]

        if not tasks_response:
            return make_response(jsonify(f"There are no tasks"))
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task.from_dict(request_body)
        except KeyError:
            return (f"Invalid data", 400)

        # Add this new instance of task to the database
        db.session.add(new_task)
        db.session.commit()

        # Successful response
        return {
            "task": new_task.to_json()
        }, 201

# Path/Endpoint to get a single task
# Include the id of the record to retrieve as a part of the endpoint
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])

# GET /task/id
def handle_task(task_id):
    # Query our db to grab the task that has the id we want:
    task = Task.query.get(task_id)

    if request.method == "GET":
        return task.to_json(), 200
    elif request.method == "PUT":
        request_body = request.get_json()

        task.update(request_body)

        # Update this task in the database
        db.session.commit()

        # Successful response
        return {
            "task": task.to_json()
        }, 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

    return {
        "details": f'Task {task.task_id} \"{task.title}\" successfully deleted',
    }, 202

# PATCH /task/id/mark_complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    task = get_record_by_id(Task, task_id)
    task.completed_at = date.today()

    db.session.commit()

    return task.to_json(), 200


# PATCH /task/id/mark_incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = get_record_by_id(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return task.to_json(), 200
