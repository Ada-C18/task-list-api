from flask import Blueprint, request, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    # Feel free to add a guard clause
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    # How we know about Dog
    new_task = Task(
        # You're looking for this key and assign it to name, breed, gender, age
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )

    # Add this new instance of dog to the database
    db.session.add(new_task)
    db.session.commit()

    # Successful response
    return make_response(f"Task {new_task.title} has been successfully created!", 201)
