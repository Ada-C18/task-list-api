from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"Message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"Message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def create_slack_bot_message(task):
    URL = 'https://slack.com/api/chat.postMessage'
    SLACK_API_KEY = os.environ.get("SLACK_TOKEN")

    slack_params = {
        "channel": "C0499FWAQ5D",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_headers ={
        "Authorization": SLACK_API_KEY
    }

    requests.post(URL, data=slack_params, headers=slack_headers)

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods =["GET"])
def read_all_tasks(): 
    tasks = Task.query.all()
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    sorting_type = request.args.get("sort")
    if sorting_type == "asc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"]))
    elif sorting_type == "desc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"], reverse=True))
    else: 
        return jsonify(tasks_response)

@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task(title=request_body["title"], 
                    description=request_body["description"])
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_dict()}, 201)
    
@tasks_bp.route("/<task_id>", methods =["GET"])
def read_one_task(task_id):
    task = validate_model(Task,task_id)
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    create_slack_bot_message(task)
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task":task.to_dict()}

# ---------- GOALS ROUTES (Wave 5) --------------
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods =["POST"])
def create_goal():
    request_body = request.get_json()
    try: 
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    db.session.add(new_goal)
    db.session.commit()
    return make_response({"goal":new_goal.to_dict()}, 201)

@goals_bp.route("", methods =["GET"])
def read_all_goals(): 
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods =["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return {"goal":goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return {"goal":goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())
    result = goal.to_dict()
    result["tasks"] = tasks_response
    
    return jsonify(result)

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks_id_list = request_body["task_ids"]
    for task_id in tasks_id_list:
        task = validate_model(Task, task_id)
        task.goal_id = goal_id
        db.session.commit()
    return {"id": int(goal_id), "task_ids" : tasks_id_list}
