from os import abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import datetime 
import requests
import os 

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_list_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    list_task_id = []

    for task_id in request_body["task_ids"]:
        list_task_id.append(task_id)
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
        db.session.commit()
    new_goal = {
        "id" : goal.goal_id,
        "task_ids" : list_task_id
    }

    return jsonify (new_goal), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def rad_all_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    try:
        response_body = {
            "id":goal.goal_id,
            "title": goal.title,
            "tasks": [task.to_dict() for task in goal.tasks]
        }
        for task in response_body["tasks"]:
            task["goal_id"] = goal.goal_id

        # return make_response(jsonify(response_body), 200)
    except:
        response_body = {
            "id":goal.goal_id,
            "title": goal.title,
            "tasks": []
        }

    return jsonify(response_body), 200


@goals_bp.route("", methods=["POST"])
def add_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_json(Goal, request_body)
        db.session.add(new_goal)
        db.session.commit()
        goals_response = {}
        goal_in_dict = new_goal.to_dict()
        goals_response["goal"] = goal_in_dict

        return jsonify (goals_response), 201

    except:
        response_body = {}
        response_body["details"] = "Invalid data"

        return response_body, 400

@tasks_bp.route("", methods=["POST"])
def add_task():
    try:
        request_body = request.get_json()
        if "completed_at" not in request_body:
            request_body["completed_at"] = None

        new_task = Task.from_json(Task, request_body)
        db.session.add(new_task)
        db.session.commit()
        tasks_response = {}
        task_in_dict = new_task.to_dict()
        tasks_response["task"] = task_in_dict

        return jsonify (tasks_response), 201

    except:
        response_body = {}
        response_body["details"] = "Invalid data"

        return response_body, 400

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify (goals_response), 200

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("completed_at")
    sort_query = request.args.get("sort")

    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    elif completed_query:
        tasks = Task.query.filter_by(completed_at=completed_query)
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify (tasks_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goals_response = {}
    goal_in_dict = goal.to_dict()
    goals_response["goal"]=goal_in_dict

    return jsonify (goals_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict

    return jsonify (tasks_response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    goals_response = {}
    goal_in_dict = goal.to_dict()
    goals_response["goal"]=goal_in_dict

    return jsonify (goals_response), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict

    return jsonify (tasks_response), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    response_body = {}
    response_body["details"] = (f'Goal {goal_id} "{goal.title}" successfully deleted')

    return response_body, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    response_body = {}
    response_body["details"] = (f'Task {task_id} "{task.title}" successfully deleted')

    return response_body, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()
    slack_bot(f"Someone just completed the task {task.title}")
    task_in_dict = task.to_dict()
    task_in_dict["is_complete"] = True
    tasks_response = {"task" : task_in_dict}

    return jsonify (tasks_response), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict

    return jsonify (tasks_response), 200

# slack bot helper func
def slack_bot(msg):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

    query_params = {
        "channel" : "#task-notifications",
        "text" : msg
    }
    headers = {
        "Authorization" : f"Bearer {SLACK_API_KEY}"
    }

    requests.post(PATH, params=query_params, headers=headers)

# verify id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model