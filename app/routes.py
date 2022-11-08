from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"details": f"{cls.__name__} {id} invalid"}, 400))

    query_result = cls.query.get(id)
        
    if query_result is None:
        abort(make_response({"message": f"{cls.__name__} {id} not found."}, 404))

    return query_result

def send_msg_to_slack(cls, id):
    path = "https://slack.com/api/chat.postMessage"
    SLACK_AUTHENTICATION = os.environ.get("SLACK_AUTHENTICATION")

    query_params = {
        "channel": "task-notifications", 
        "text": f"Someone just completed the task {cls.title}", 
    }        
    header = {   
    "Authorization" : SLACK_AUTHENTICATION
        }
    
    result = requests.post(path, data = query_params, headers=header)

    
@tasks_bp.route("", methods = ["POST"])
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return make_response(jsonify(new_task.to_task_dict())), 201

    except:
        if not (request_body.get("title") is None):
            abort(make_response({"details": "Invalid data"}, 400))

        if not (request_body.get("description") is None):
            abort(make_response({"details": "Invalid data"}, 400))


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    title_query = request.args.get("title")
    sort_type = request.args.get("sort")    

    if title_query is not None:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_type == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_type == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_list = [t.to_dict() for t in tasks]
    
    return jsonify(task_list), 200


@tasks_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_id(Task, id)

    return jsonify(task.to_task_dict()), 200

    
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_id(Task, id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify(task.to_task_dict())), 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def update_completed_task(id):
    task = validate_id(Task, id)

    task.completed_at = datetime.utcnow()

    db.session.commit()

    send_msg_to_slack(task, id)

    return make_response(jsonify(task.to_task_dict())), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def update_incomplete_task(id):
    task = validate_id(Task, id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify(task.to_task_dict())), 200

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_id(Task, id)

    db.session.delete(task)

    db.session.commit()

    return make_response({'details': f'Task {id} "{task.title}" successfully deleted'})

@goals_bp.route("", methods = ["POST"])
def create_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        return make_response(jsonify(new_goal.goal_to_dict())), 201

    except:
        if not (request_body.get("title")):
            abort(make_response({"details": "Invalid data"}, 400))

@goals_bp.route("", methods=["GET"])
def get_all_goals():
   
    goals = Goal.query.all()

    goals_list = [g.to_dict() for g in goals]
    
    return jsonify(goals_list), 200

@goals_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    goal = validate_id(Goal, id)

    return jsonify(goal.goal_to_dict()), 200

@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_id(Goal, id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return make_response(jsonify(goal.goal_to_dict())), 200

@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_id(Goal, id)

    db.session.delete(goal)

    db.session.commit()

    return make_response({'details': f'Goal {id} "{goal.title}" successfully deleted'})

@goals_bp.route("/<id>/tasks", methods=["POST"])
def create_task(id):

    goal = validate_id(Goal, id)
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    new_task.goal = goal

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_task_dict())), 200

@goals_bp.route("/<id>/tasks", methods=["GET"])
def get_tasks(id):

    goal = validate_id(Goal, id)
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    return make_response(jsonify(tasks_response)), 200
