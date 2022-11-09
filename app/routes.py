from app import db
from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import date
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query
    sort_query = request.args.get("sort") 

    if sort_query == "asc":
        tasks = task_query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = task_query.order_by(desc(Task.title)).all()
    else:
        tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)

    return {"task":task.to_dict()}


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))
    else:
        return task


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}))


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)


@tasks_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def update_complete(task_id, complete):
    task = validate_task_id(task_id)

    if complete == "mark_complete":
        task.is_complete = True
        task.completed_at = date.today()
        slack_post(task_id)

    elif complete == "mark_incomplete":
        task.is_complete = False
        task.completed_at = None

    db.session.commit()

    return make_response({"task":task.to_dict()}, 200)


def slack_post(task_id):
    task = validate_task_id(task_id)
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ.get('API_KEY'),
        'channel': 'C049FQLJTBN',
        'text': f'Someone just completed the task {task.title}'}).json()


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)


@goals_bp.route("", methods=["GET"])
def get_all_goal():
    goals = Goal.query.all()
    goal_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)

    return {"goal": goal.to_dict()}


def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))
    else:
        return goal


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal":goal.to_dict()}, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()  

    for task_id in request_body['task_ids']:  
        task = Task.query.get(task_id)  
        task.goal_id = goal.goal_id  

    db.session.commit()

    response = {"id": goal.goal_id,
                "task_ids": request_body['task_ids']}

    return make_response(response, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_goal_id(goal_id)

    tasks = [Task.to_dict(task) for task in goal.tasks]
    response = {
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks
    }

    return make_response(response, 200)
