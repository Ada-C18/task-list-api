import datetime
import requests
import os
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, abort, request

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")
task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, id):
    try:
        model_id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return model

#==============================
#         GOAL ROUTES
#==============================
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.instance_from_json(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return {"goal": goal.to_dict()}

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}))

#==============================
#         TASK ROUTES
#==============================
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.instance_from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())    #STOPPED HERE
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())    #STOPPED HERE
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return {"task": task.to_dict()}

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}))

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.datetime.now()

    post_message_to_slack(task)

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

def post_message_to_slack(a_task):
    token = os.environ.get("SLACKBOT_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    auth_header = {'Authorization': token}
    param_data = {"channel":"task-notifications",
                "text":f"Someone just completed the task {a_task.title}"}

    requests.post(url, headers = auth_header, data=param_data)