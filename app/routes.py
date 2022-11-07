from datetime import datetime
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')
goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    else:
        return model

def validate_input_data(data_dict):
    try:
        return Task.from_dict(data_dict)
    except KeyError:
        abort(make_response(jsonify(dict(details="Invalid data")), 400))

# TASK MODEL
# create a task (POST)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = validate_input_data(request_body)

    if not new_task.title or not new_task.description:
        return make_response({"details": f"Invalid data"})

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# read one task (GET)
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)

    return jsonify({"task": task.to_dict()}), 200
    
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


# replace a task (PUT)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()
    
    response = {"task": task.to_dict()}
    return response


# update a task (PATCH)
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.utcnow()

    db.session.commit()
   
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomple_task(id):
    task = validate_model(Task, id)

    task.completed_at = None

    db.session.commit()
   
    return jsonify({"task": task.to_dict()}), 200


# delete a task (DELETE)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    int_id = int(id)
    description = str(task.description )
    db.session.delete(task)
    db.session.commit()

    # Returns error 
    return(make_response({"details": f"Task {int_id} {description} successfully deleted"}), 200)


# GOAL MODEL 
# create a goal (POST)
@tasks_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = validate_input_data(request_body)

    if not new_goal.title:
        return make_response({"details": f"Invalid data"})

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# read one goal (GET)
@goals_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = validate_model(Goal, id)

    return jsonify({"goal": goal.to_dict()}), 200
    
# read all goals (GET)
@goals_bp.route("", methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)
    

