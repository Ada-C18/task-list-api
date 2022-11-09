from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model_by_id(cls, model_id):
    '''Helper function to validate database IDs prior to executing queries.'''
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"msg": f"{model_id} is not valid"}, 400))
    
    object = cls.query.get(model_id)

    if object is None:
        return abort(make_response({"msg": f"{model_id} not found"}, 404))

    return object


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    '''Gets all tasks from the task table in the database.'''
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    response = []
    for task in tasks:
            response.append(task.to_dict())
    
    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    '''Creates a new task, requires title and description, id will be autogenerated.'''
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
            
    except Exception as e:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task_by_id(task_id):
    '''Get one task by id, validates id before executing query.'''
    task = validate_model_by_id(Task, task_id)

    if task.goal_id:
        return {"task": 
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete(),
                "goal_id": task.goal_id
                }
            }
    else: 
        return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task_by_id(task_id):
    '''Update a task by id, id validated before executing request.'''
    request_body = request.get_json()
    task = validate_model_by_id(Task, task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    '''Delete a task by id, id validated before executing request.'''
    task = validate_model_by_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"}), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    '''Updating task to completed using datetime function. Task ID validated before executing request.
    Sends message of completion to slack channel task-notifications.'''
    
    task = validate_model_by_id(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    # slack api call to post to task-notifications
    slack_oauth_token = os.environ.get("SLACK_OAUTH_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    headers = {"Authorization": f"Bearer {slack_oauth_token}"}

    requests.patch(url=url, params=params, headers=headers)

    return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    '''Marks a task as incomplete by id. ID validated before request.'''
    task = validate_model_by_id(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


####################Goal routes###################

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    '''Creates a new goal, requires title, id will be autogenerated.'''
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except Exception as e:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    '''Gets all goals from the task table in the database.'''
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    
    response = []
    for goal in goals:
            response.append(goal.to_dict())
    
    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal_by_id(goal_id):
    '''Get one goal by id, validates id before executing query.'''
    goal = validate_model_by_id(Goal, goal_id)
    return {"goal": goal.to_dict()}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal_by_id(goal_id):
    '''Update a goal by id, id validated before executing request.'''
    request_body = request.get_json()
    goal = validate_model_by_id(Goal, goal_id)

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    '''Delete a goal by id, id validated before executing request.'''
    goal = validate_model_by_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_all_tasks_by_goal_id(goal_id):
    '''Returns list of task objects for task_ids in goal.tasks.'''
    goal = validate_model_by_id(Goal, goal_id)

    tasks = []
    for task in goal.tasks:
        tasks.append(task.to_dict())
    
    return jsonify({
        "id": goal.goal_id,
        "title": "Build a habit of going outside daily",
        "tasks": tasks
    }), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_existing_tasks_to_goal_id(goal_id):
    '''Updates goal with list of tasks.'''
    request_body = request.get_json()
    goal = validate_model_by_id(Goal, goal_id)
    
    provided_task_ids = request_body["task_ids"]
    
    tasks = goal.tasks
    task_ids = []
    for task_id in provided_task_ids:
        task = validate_model_by_id(Task, task_id)
        if task:
            tasks.append(task)
            task_ids.append(task.task_id)

    goal.tasks = tasks

    db.session.commit()
    
    return jsonify({
        "id": goal.goal_id,
        "task_ids": task_ids
        })
