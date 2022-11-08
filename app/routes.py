from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime
import os
import requests

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# -------- Helper functions ---------
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"Message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"Message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

def delete_model(cls, model_id):
    model = validate_model(cls,model_id)
    db.session.delete(model)
    db.session.commit()
    return make_response({"details": f'{cls.__name__} {model_id} "{model.title}" successfully deleted'})

def read_one_model(cls, model_id):
    model = validate_model(cls,model_id)
    return {cls.__name__.lower():model.to_dict()}

def create_new_model(cls, model_data):
    try: 
        new_model = cls.from_dict(model_data)
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    db.session.add(new_model)
    db.session.commit()
    return make_response({cls.__name__.lower():new_model.to_dict()}, 201)
    
def create_slack_bot_message(task):
    URL = 'https://slack.com/api/chat.postMessage'
    slack_params = {
        "channel": "C0499FWAQ5D",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_headers ={
        "Authorization": os.environ.get("SLACK_TOKEN")
    }
    requests.post(URL, data=slack_params, headers=slack_headers)

# --------- TASK ENDPOINTS --------------
@tasks_bp.route("", methods =["GET"])
def read_all_tasks(): 
    tasks_response = [task.to_dict() for task in Task.query.all()]
    sorting_type = request.args.get("sort")
    if sorting_type == "asc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"]))
    elif sorting_type == "desc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"], reverse=True))
    else: 
        return jsonify(tasks_response)

@tasks_bp.route("", methods =["POST"])
def create_task():
    return create_new_model(Task, request.get_json())
    
@tasks_bp.route("/<task_id>", methods =["GET"])
def read_one_task(task_id):
    return read_one_model(Task, task_id)

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
    return delete_model(Task, task_id)

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

# ---------- GOALS ENDPOINTS --------------

@goals_bp.route("", methods =["POST"])
def create_goal():
    return create_new_model(Goal, request.get_json())

@goals_bp.route("", methods =["GET"])
def read_all_goals(): 
    goals_response = [goal.to_dict() for goal in Goal.query.all()]
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods =["GET"])
def read_one_goal(goal_id):
    return read_one_model(Goal,goal_id)
    
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return {"goal":goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    return delete_model(Goal, goal_id)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    tasks_response = [task.to_dict() for task in goal.tasks]
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
    return {"id": goal.goal_id, "task_ids" : tasks_id_list}