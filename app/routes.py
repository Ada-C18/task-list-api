from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, request, jsonify, make_response, abort
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#========HELPER FUNCTION=======================================
def get_model_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"details":"Invalid data"}, 400))
    
    chosen_object = cls.query.get(model_id)

    if chosen_object is None:
        return abort(make_response({"msg":
        f"Could not find {cls.__name__} with id:{model_id}"}, 404))
    return chosen_object

#===============TASKS ROUTES====================================
@tasks_bp.route("", methods=["POST"])
def create_task():   
    try:
        request_body = request.get_json()
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
            )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"task":new_task.to_dict()}), 201
    
    except KeyError:
        return jsonify({"details":"Invalid data"}), 400

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query_value = request.args.get("sort")
    
    if sort_query_value == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    result = []
    for item in tasks:
        result.append(item.to_dict())
    return jsonify(result), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_model_from_id(Task, task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    update_task = get_model_from_id(Task, task_id)
    request_body = request.get_json()

    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        return jsonify({"msg": "Missing required data"}), 400
    
    db.session.commit()

    return jsonify({"task":update_task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_model_from_id(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details":
    f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_one_task_complete(task_id):   
    task_to_mark_complete = get_model_from_id(Task, task_id)
    
    task_to_mark_complete.completed_at = datetime.today()
    db.session.commit()

    #Request
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization":f"Bearer {SLACK_TOKEN}"}
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_to_mark_complete.title}"
    }
    requests.post(path, params=query_params, headers=headers)

    return jsonify({"task":task_to_mark_complete.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_incomplete(task_id):  
    task_to_mark_incomplete = get_model_from_id(Task, task_id)
    
    task_to_mark_incomplete.completed_at = None
    db.session.commit()
    
    return jsonify({"task":task_to_mark_incomplete.to_dict()}), 200

#===============GOALS ROUTES====================================
@goals_bp.route("", methods=["POST"])
def create_goal():   
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title=request_body["title"]
            )
        db.session.add(new_goal)
        db.session.commit()

        return jsonify({"goal":new_goal.to_dict()}), 201
    
    except KeyError:
        return jsonify({"details":"Invalid data"}), 400

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_model_from_id(Goal, goal_id)
    return jsonify({"goal":chosen_goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal_to_update = get_model_from_id(Goal, goal_id)
    request_body = request.get_json()

    try:
        goal_to_update.title = request_body["title"]
    except KeyError:
        return jsonify({"msg": "Missing required data"}), 400
    
    db.session.commit()

    return jsonify({"goal":goal_to_update.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = get_model_from_id(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({"details":
    f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'})

#=========NESTED ROUTES==========================
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def adding_task_ids_to_goal(goal_id):
    goal = get_model_from_id(Goal, goal_id)

    request_body = request.get_json()

    task_list = []

    for task_id in request_body["task_ids"]:
        task = get_model_from_id(Task, task_id)
        task.goal = goal
        task_list.append(task_id)

    db.session.commit()

    return jsonify({
        "id": goal.goal_id,
        "task_ids": task_list
    })

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_one_goal(goal_id):
    goal = get_model_from_id(Goal, goal_id)

    tasks = goal.get_tasks_list()
    
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks":tasks
        }), 200
