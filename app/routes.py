from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import date
import requests
import os


def validate_model(cls, model_id):
    model = cls.query.get(model_id)
   
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# ************************* CRUD ROUTES FOR TASKS ****************************************

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body.get("title") and request_body.get("description"):
        new_task = Task.from_json(request_body)
    else:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_json()}), 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    
    tasks_response = [task.to_json() for task in tasks]
    
    sort_query_value = request.args.get("sort")
    tasks_response.sort(
        key=lambda task: task["title"], reverse=sort_query_value == "desc")
    
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    chosen_task = validate_model(Task, task_id)

    if not chosen_task.goal_id:
       return jsonify({"task": chosen_task.to_json()})
    else:
        response_dict = chosen_task.to_json()
        response_dict["goal_id"] = chosen_task.goal_id
        return jsonify({"task": response_dict})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = validate_model(Task, task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.commit()
    
    return jsonify({"task": chosen_task.to_json()})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    chosen_task = validate_model(Task, task_id)
    
    db.session.delete(chosen_task)
    db.session.commit()

    return jsonify({"details": f"Task {task_id} \"{chosen_task.title}\" successfully deleted"})

def call_slack_api(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    query_params = {
        "channel": "task-notifications",
        "text": text
        }

    response = requests.post(url, headers=headers, params=query_params)

    return response


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    chosen_task = validate_model(Task, task_id)
    chosen_task.completed_at = date.today()
    call_slack_api(f"Someone just completed the task {chosen_task.title}")

    db.session.commit()

    chosen_task_dict = chosen_task.to_json()
    chosen_task_dict["is_complete"] = True
    return jsonify({"task": chosen_task_dict})


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    chosen_task = validate_model(Task, task_id)
    chosen_task.completed_at = None

    db.session.commit()

    return jsonify({"task": chosen_task.to_json()})


# **************************** CRUD ROUTES FOR GOALS *****************************************

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if request_body:
        new_goal = Goal.from_json(request_body)
    else:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_json() for goal in goals]

    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    chosen_goal = validate_model(Goal, goal_id)

    return jsonify({"goal": chosen_goal.to_json()})

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    chosen_goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    try:
        chosen_goal.title = request_body["title"]
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.commit()

    return jsonify({"goal": chosen_goal.to_json()})

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    chosen_goal = validate_model(Goal, goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{chosen_goal.title}\" successfully deleted"})

# ***************************** NESTED ROUTES FOR GOALS AND TASKS *********************************

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    chosen_goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = chosen_goal.goal_id

    db.session.commit()

    return jsonify({"id": chosen_goal.goal_id, "task_ids": request_body["task_ids"]})

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
    chosen_goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_json() for task in chosen_goal.tasks]
    
    for i in range(len(tasks_response)):
        tasks_response[i]["goal_id"] = chosen_goal.goal_id

    return jsonify({"id": chosen_goal.goal_id, "title": chosen_goal.title, "tasks": tasks_response})






