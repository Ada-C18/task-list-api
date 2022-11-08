from app import db
from app.models.goal import Goal
from flask import abort, Blueprint, jsonify, make_response, request
# from dotenv import load_dotenv
# import os
from .routes import validate_task

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response_str = f"Invalid goal id {goal_id}. ID must be a integer."
        abort(make_response({"message": response_str}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        response_str = f"Goal {goal_id} not found."

        abort(make_response({"message": response_str}, 404))

    return goal


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    response = {
        "goal": chosen_goal.to_dict()
    }

    return jsonify(response)


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if request_body == {}:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal(
        title=request_body["title"],
    )

    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": new_goal.to_dict()
    }

    return response, 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    response = {
        "goal": goal.to_dict()
    }

    db.session.commit()

    return jsonify(response)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }
    # {
    #     "details": "Goal 1 \"Build a habit of going outside daily\" successfully deleted"
    # }

    # return make_response(jsonify(response))
    return jsonify(response)


# POST
# Sending a List of Task IDs to a Goal
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_task_ids_to_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    # three Tasks belong to the Goal and it gets updated in the database
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return response


# GET
# Getting Tasks of One Goal
# /goals/<goal_id>/tasks
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_goal(goal_id)

    response = goal.to_dict()

    return jsonify(response), 200

# response
# {
#   "id": 333,
#   "title": "Build a habit of going outside daily",
#   "tasks": [
#     {
#       "id": 999,
#       "goal_id": 333,
#       "title": "Go on my daily walk 🏞",
#       "description": "Notice something new every day",
#       "is_complete": false
#     }
#   ]
# }
