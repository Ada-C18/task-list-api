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
    return ({
    # "task": f'{id}',  need to figure out how to return id
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": new_task.completed_at
    },201)

@task_bp.route("", methods=["GET"])
# Change name to handle dogs
def get_all_tasks():
    task_query = Task.query

    # breed_query = request.args.get("breed")
    # if breed_query:
    #     # exact string matching - case sensitive
    #     # dog_query = dog_query.filter_by(breed=breed_query)
    #     # partial filters - case sensitive
    #     # dog_query = dog_query.filter(Dog.breed.contains(breed_query))
    #     # partial filter - case insensitive
    #     dog_query = dog_query.filter(Dog.breed.ilike(f"%{breed_query}%"))

    # age_query = request.args.get("age")
    # if age_query:
    #     dog_query = dog_query.filter_by(age=age_query)

    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        })

# Path/Endpoint to get a single dog
# Include the id of the record to retrieve as a part of the endpoint
@task_bp.route("/<task_id>", methods=["GET"])
# GET /dog/id
def get_one_task(task_id):
    # Query our db to grab the dog that has the id we want:
    task = Task.query.get(task_id)

    # Send back a single JSON object (dictionary):
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at
    }