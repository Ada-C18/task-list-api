
from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.routes_helper import get_one_obj_or_abort

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


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

    for task in request_body["task_ids"]:
        chosen_task = get_one_obj_or_abort(Task, task)
        chosen_task.goal = parent_goal

    db.session.add(chosen_task)
    db.session.commit()
    
    return jsonify({"id": int(goal_id), "task_ids": request_body["task_ids"]}), 200



@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_belonging_to_a_goal(goal_id):
    parent_goal = get_one_obj_or_abort(Goal, goal_id)
    
    task_list = []
    for task in parent_goal.tasks:
        task_list.append(task.return_body())

    response_dict = parent_goal.return_body()
    response_dict["tasks"] = task_list
    return jsonify(response_dict), 200   

