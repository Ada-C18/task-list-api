from flask import Blueprint,jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime 
import os
import requests

task_bp = Blueprint("task_bp",__name__, url_prefix="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`.Id must be an integer."
        abort(make_response(jsonify({'message':response_str}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task: 
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({'message':response_str}), 404))
    return matching_task


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"])

    db.session.add(new_task)

    db.session.commit()

    return {
        "task":{
            "id" : new_task.id,
            "title" : new_task.title,
            "description" : new_task.description,
            "is_complete" : new_task.is_complete
        }
    }, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("title")

    sort_param = request.args.get("sort")

    if not title_param:
        tasks = Task.query.all()
    
    if sort_param  == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()

    response = [task.to_dict() for task in tasks]
    return jsonify(response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    task_dict = {
        "task":{
            "id" : chosen_task.id,
            "title" : chosen_task.title,
            "description" : chosen_task.description,
            "is_complete" : chosen_task.is_complete
        }
    }
        
    return jsonify(task_dict), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message": "Request must include title and description."}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"] 

    db.session.commit()

    return {
        "task":{
            "id" : chosen_task.id,
            "title" : chosen_task.title,
            "description" : chosen_task.description,
            "is_complete" : chosen_task.is_complete
        }
    }, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)

    db.session.delete(chosen_task)

    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}), 200


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_is_complete(task_id):
    update_is_valid_id = get_one_task_or_abort(task_id)

    update_is_valid_id.completed_at = datetime.today()
    db.session.add(update_is_valid_id)
    db.session.commit()

    SLACK_PATH = "https://slack.com/api/chat.postMessage"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    
    headers = {
        "Authorization" : f"Bearer {SLACK_BOT_TOKEN}"
        }
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {update_is_valid_id.title}"
        }

    requests.get(url=SLACK_PATH, headers=headers, params=params)


    return jsonify({"task":Task.to_dict(update_is_valid_id)}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incompete(task_id):
    task_incompete = get_one_task_or_abort(task_id)
    task_incompete.completed_at = None

    db.session.add(task_incompete)
    db.session.commit()

    return jsonify({"task":Task.to_dict(task_incompete)}), 200


# ###################################################################
goal_bp = Blueprint("goal_bp",__name__, url_prefix="/goals")

def get_one_goal_or_abort(id):
    try:
        id = int(id)
    except ValueError:
        response_str = f"Invalid id: `{id}`.Id must be an integer."
        abort(make_response(jsonify({'message':response_str}), 400))

    matching_goal = Goal.query.get(id)

    if not matching_goal: 
        response_str = f"Goal with id {id} was not found in the database."
        abort(make_response(jsonify({'message':response_str}), 404))
    return matching_goal

@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(
        title = request_body["title"])

    db.session.add(new_goal)

    db.session.commit()

    return {
        "goal":{
            "id" : new_goal.goal_id,
            "title" : new_goal.title
        }
    }, 201


@goal_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()

    response = [Goal.to_dict(goal) for goal in goals]
    return jsonify(response), 200


@goal_bp.route("/<id>", methods=["GET"])
def get_one_goal(id):
    chosen_goal = get_one_goal_or_abort(id)
    goal_dict = {
        "goal":{
            "id" : chosen_goal.goal_id,
            "title" : chosen_goal.title
        }
    }
        
    return jsonify(goal_dict), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_task(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
            return jsonify({"message": "request must include title."}), 400

    chosen_goal.title = request_body["title"]

    db.session.commit()

    return {
        "goal":{
            "id" : chosen_goal.goal_id,
            "title" : chosen_goal.title
        }
    }, 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)

    db.session.delete(chosen_goal)

    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{chosen_goal.title}" successfully deleted'}), 200

# ###################################################################

# POST
# @goal_bp.route("/<goal_id>/tasks", methods=["POST"])
# def post_task_ids_to_goal(goal_id):
#     # tasks is a list 
#     # check if a goal 
#     # check if a task 
#     # do request 

#     request_body = request.get_json()

#     new_goal_with_task = {
#         "task_ids": 
#         }
    


#     db.session.add(new_goal_with_task)

#     db.session.commit()

#     return {
#             "id" : new_goal_with_task.goal_id,
#             "task_ids" : new_goal_with_task. # ????????
#         }, 201

# # GET 