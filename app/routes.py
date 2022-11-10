from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes_helper import get_one_obj_or_abort
from datetime import datetime
import requests, os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# ******** Wave 1 ********
@task_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()

    # new_task = Task.from_dict(request_body)
    if "title" not in response_body or\
        "description" not in response_body:
        # “is_complete” not in respnse_body
        return jsonify({"details": "Invalid data"}), 400
    new_task = Task(
        title = response_body["title"],
        description = response_body["description"],)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201
# ******** Wave 2 ********
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    title_param = request.args.get("sort") 

    if title_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    elif title_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    
    chosen_task = get_one_obj_or_abort(Task, task_id)

    return jsonify({
        "task": chosen_task.to_dict()}), 200


@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_with_new_vals(task_id):

    chosen_task = get_one_obj_or_abort(Task, task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message":"Request must include title, description"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]


    db.session.commit()

    return jsonify({f"task": chosen_task.to_dict()}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    db.session.delete(chosen_task)

    db.session.commit()

    return jsonify({"details": f'Task {chosen_task.task_id} "{chosen_task.title}" successfully deleted'}), 200

# def check_is_complete(self):
#         if self.completed_at:
#             return True
#         else:
#             return False 

# ******** Wave 3 ********

@task_bp.route("<task_id>/mark_complete", methods=["PATCH"])
def mark_complite_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = datetime.now()
    db.session.commit()
    
    PATH = "https://slack.com/api/chat.postMessage"
    
    SLACKBOT_TOKEN = os.environ.get("SLACKBOT_TOKEN")

    query_params = {
        "token": SLACKBOT_TOKEN,
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url=PATH, data=query_params, headers={"Authorization": SLACKBOT_TOKEN})
    
    return jsonify({"task":chosen_task.to_dict()}), 200

@task_bp.route("<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplite_task(task_id):
    chosen_task = get_one_obj_or_abort(Task,task_id)
    task = Task.query.get(task_id)
    if task is None:
        return make_response("The task was not found", 404)
    task.completed_at = None
    db.session.commit()
    return jsonify({"task":chosen_task.to_dict()}), 200

# ******** Wave 5 ********
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    response_body = request.get_json()

    if "title" not in response_body:
        return jsonify({"details": "Invalid data"}), 400
    new_goal = Goal(
        title = response_body["title"],
        )

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    
    goals = Goal.query.all()

    response = [goal.to_dict() for goal in goals]

    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    return jsonify({
        "goal": chosen_goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_with_new_vals(goal_id):

    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    if "title" in request_body:
        # return jsonify({"details":"Request must include title"}), 400
        chosen_goal.title = request_body["title"]   

    db.session.commit()

    return jsonify({f"goal": chosen_goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    db.session.delete(chosen_goal)

    db.session.commit()

    return jsonify({"details": f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'}), 200

# ******** Wave 6 ********

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_belonging_to_a_goal(goal_id):
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)

    tasks_list = []
    for task in chosen_goal.tasks:
        tasks_list.append(task.to_dict())

    # tasks_response = [task.to_dict() for task in goal.tasks]
    response_dict = chosen_goal.to_dict()
    response_dict["tasks"] = tasks_list
    return jsonify(response_dict), 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_belonging_to_a_goal(goal_id):
    parent_goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    for task in request_body["task_ids"]:
        select_task = get_one_obj_or_abort(Task,task)
        select_task.goal = parent_goal
        
        db.session.add(select_task)
        db.session.commit()


    return jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200