import requests, os
from datetime import datetime
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes_helper import get_one_obj_or_abort


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


# Create a Task: Valid Task With null completed_at
@task_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()

    if "title" not in response_body or\
       "description" not in response_body or\
       "completed_at" not in response_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(response_body)
       
    db.session.add(new_task)
    db.session.commit()

    # using the class method in task.py 
    return jsonify({"task":new_task.return_body()}), 201


# Get Tasks: Getting Saved Tasks, sorting by ascending/descending
@task_bp.route("", methods=["GET"])
def read_task():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    response = [task.return_body() for task in tasks]
    return jsonify(response), 200   



# Get One Task: One Saved Task
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    return jsonify({"task":chosen_task.return_body()}), 200


# Update Task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    request_body = request.get_json()
    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200

    

# Deleting a Task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_one_obj_or_abort(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'}), 200

 
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_update(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = datetime.now()
    db.session.commit()
    
    PATH = "https://slack.com/api/chat.postMessage"
    
    SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")

    # the query parameters come from the 
    query_params = {
        "token": SLACKBOT_TOKEN,
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url=PATH, data=query_params, headers={"Authorization": SLACKBOT_TOKEN})
    # POST: to submit data to be processed to the server.
    
    return jsonify({"task":chosen_task.return_body()}), 200


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_update(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = None
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200
    

# helper function to check the value of completed_at
# def check_task_status(goal_id, result):
#     chosen_task = validate_task(goal_id)
#     task = Task.query.get(goal_id)
#     if task is None:
#         return make_response("The task was not found", 404)
#     task.complete_at = result
#     db.session.commit()
#     return jsonify({"task":chosen_task.return_body()}), 200





# create goal
@goal_bp.route("", methods=["POST"])
def create_goal():
    response_body = request.get_json()

    if "title" not in response_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(title = response_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.return_body()}), 201


# Get Goals
@goal_bp.route("", methods=["GET"])
def read_goal():
    goals = Goal.query.all()
    response = [goal.return_body() for goal in goals]
    return jsonify(response), 200   


# Get One Goal
@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    chosen_goal= get_one_obj_or_abort(Goal, goal_id)
    return jsonify({"goal":chosen_goal.return_body()}), 200


# Update Goal
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    request_body = request.get_json()

    chosen_goal.title = request_body["title"]
    
    db.session.commit()
    return jsonify({"goal":chosen_goal.return_body()}), 200


# Delete Goal
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'}), 200




# ==================================================
# One-to-Many Relationship bewteen goals and tasks
# ==================================================

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_belonging_to_a_goal(goal_id):
    parent_goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    new_task = Task.from_dict(request_body)
    new_task.goal = parent_goal

    db.session.add(new_task)
    db.session.commit()

    return jsonify({f"id": {new_task.goal.goal_id}, "task_ids": {new_task.task_id}}), 201