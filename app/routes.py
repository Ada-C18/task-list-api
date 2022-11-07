from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = [task.to_json() for task in tasks]

        if not tasks_response:
            return make_response(jsonify(f"There are no tasks"))
        return jsonify(tasks_response), 200

    elif request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task(
                title = request_body['title'],
                description = request_body['description'],
                completed_at = request_body['completed_at']
            )
        except KeyError:
            return (f"Invalid data", 400)

        # Add this new instance of task to the database
        db.session.add(new_task)
        db.session.commit()

        # Successful response
        return make_response(f"Task {new_task.title} has been successfully created!", 201)

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

        # Updated task attributes are set:
        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']

        # Update this task in the database
        db.session.commit()

        # Sucessful response
        return make_response(f"task {task.title} has been successfully updated!", 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

        return make_response(f"task {task.title} successfully deleted", 202)