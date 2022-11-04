from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#***********************************************#
#***************** Task Routes *****************#
#***********************************************#

@tasks_bp.route("", methods=["POST"])
def add_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )

        db.session.add(new_task)
        db.session.commit()

    except:
        response_body = {
            "details": "Invalid data"
        }

        abort(make_response(jsonify(response_body), 400))
    
    return jsonify(generate_response_body(Task, new_task)), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    order = request.args.get("sort")

    if order is None:
        tasks = Task.query.all()
    elif order == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif order == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    return jsonify(generate_response_body(Task, tasks)), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify(generate_response_body(Task, task)), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify(generate_response_body(Task, task)), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }

    return jsonify(response_body), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_one_task_as_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    return jsonify(generate_response_body(Task, task)), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_as_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify(generate_response_body(Task, task)), 200

#***********************************************#
#***************** Goal Routes *****************#
#***********************************************#

@goals_bp.route("", methods=["POST"])
def add_one_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"]
        )

        db.session.add(new_goal)
        db.session.commit()

    except:
        response_body = {
            "details": "Invalid data"
        }

        abort(make_response(jsonify(response_body), 400))
    
    return jsonify(generate_response_body(Goal, new_goal)), 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    return jsonify(generate_response_body(Goal, goals)), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify(generate_response_body(Goal, goal)), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return jsonify(generate_response_body(Goal, goal)), 200

#************************************************#
#*************** Helper Functions ***************#
#************************************************#

def generate_response_body(cls, models):
    """
    Return a list of model-detail dictionaries if @param models is a list of Model objects
    Return a single dictionary {"model": model-detail} if @param models is a Model object
    """
    if isinstance(models, list):
        response = []

        for model in models:
            response.append(cls.to_dict(model))

        return response
    
    else:
        return {
            f"{cls.__name__}".lower(): cls.to_dict(models)
        }


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response_body = {
            "message": f"{cls.__name__} id {model_id} is invalid."
        }

        abort(make_response(jsonify(response_body), 400))
    
    model = cls.query.get(model_id)

    if model is None:
        response_body = {
            "message": f"{cls.__name__} {model_id} is does not exist."
        }

        abort(make_response(jsonify(response_body), 404))

    return model