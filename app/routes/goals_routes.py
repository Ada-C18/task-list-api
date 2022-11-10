from flask import Blueprint, jsonify, request
from app import db
from app.models.goal import Goal
from .helper_function import get_one_obj_or_abort
from app.models.task import Task

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

#---------------------------POST-------------------------------------------- 
@goal_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    if "title" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(
        title = request_body["title"],
    )
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.make_dict()}), 201 

#--------------------------------------GET------------------------------------
@goal_bp.route("", methods=["GET"])
def get_all_goals():

    goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.make_dict())
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):

    goal = get_one_obj_or_abort(Goal, goal_id)

    return jsonify({"goal": goal.make_dict()}), 200

#--------------------------------PUT-------------------------
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_values(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
            return jsonify({"details": "Invalid data"})

    goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.make_dict()}), 200

#-------------------------DELETE----------------------------
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def detlete_one_goal(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_belonging_to_a_goal(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)

    response = [task.create_dict() for task in goal.tasks]
    goal_dict = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": response
        }

    return jsonify(goal_dict), 200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_belonging_to_a_goal(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        task.goal_id = goal_id

        db.session.add(task)
        db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200