from datetime import datetime
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
         abort(make_response(jsonify({"message":f"task {model_id} not found"}), 400))
    
    model = cls.query.get(model_id)
    if not model:
        # getting error about built-in function {model_id}
        abort(make_response(jsonify({"message":f"task {model_id} not found"}), 404))
    return model

def validate_input_data(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))

# ---------------------------------
# create a task (POST)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # new_task = Task.from_dict(request_body)
    new_task = validate_input_data(request_body)

    db.session.add(new_task)
    db.session.commit()

   
    return make_response({"task": new_task.to_dict()}, 201)

# ---------------------------------
# read one task (GET)
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)

    return jsonify({"task": task.to_dict()}), 200
    

# ---------------------------------
# read all tasks (GET)
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_asc_query = request.args.get("sort")

    if sort_asc_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_asc_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

# ---------------------------------
# replace a task (PUT)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    response = {"task": task.to_dict()}
    return response


# update a task (PATCH)
# not required- might not be correct, but hopefully helps CRUD
# when I send a `PATCH` request to `/tasks/1/mark_complete`
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def patch_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.utcnow

    db.session.commit()
   
    return jsonify({"task": task.to_dict()}), 200


# delete a task (DELETE)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()

    # Return error because we referenced to task.id after it has been deleted!!
    response = make_response({"details": f"Task {task.id} {task.description} successfully deleted"}, 200)
    return response

