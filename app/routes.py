from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
import requests, os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model_id(Task, task_id)

    return make_response(jsonify({"task": task.to_dict()})), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model_id(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model_id(Task, task_id)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    SLACK_API_TOKEN = os.environ.get("BOT_TOKEN")
    channel_id = "task-notifications"

    query_params = {
        "channel": channel_id,
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(path, params=query_params, headers={"Authorization": f"Bearer {SLACK_API_TOKEN}"})

    return make_response(jsonify({"task": task.to_dict()}), 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model_id(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)

###################helper function############################
def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))
    
    chosen_object = cls.query.get(model_id)

    if not chosen_object:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return chosen_object


#########goal routes############

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    return make_response(jsonify({"goal": goal.to_dict()})), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200)