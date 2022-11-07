from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import datetime as dt
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

#Helper Functions 
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))
        
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))
        
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} not found"}, 404))

    return goal

def slack_bot_msg(task_title):

    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
    my_headers = {'Authorization' : 'Bearer '+SLACK_TOKEN}
    query_params ={
        "channel": "task-notifications",
        "text": (f"Someone just completed the task {task_title}.")
    }

    requests.post(PATH, params=query_params, headers=my_headers)


#Task routes
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_param=request.args.get("sort")
    if sort_param == "asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks=Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }), 200
    return jsonify(tasks_response),200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():  
    request_body = request.get_json()      
    if ("title" not in request_body) or ("description" not in request_body):
        return jsonify({
            "details": "Invalid data"
        }), 400
    else:
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}), 201
    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return jsonify ({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }), 200)



@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = (dt.date.today())
    db.session.commit()
    slack_bot_msg(task.title)
    return jsonify ({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = (None)
    db.session.commit()
    return jsonify ({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}), 200

#Goal Routes
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals=Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title,
            }), 200
    return jsonify(goals_response),200

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return jsonify({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title,
            }}), 200

@goals_bp.route("", methods=["POST"])
def create_goal():  
    request_body = request.get_json()      
    if ("title" not in request_body):
        return jsonify({
            "details": "Invalid data"
        }), 400
    else:
        request_body = request.get_json()
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()
        return jsonify({
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }}), 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify ({
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def goal_task(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        }), 200)