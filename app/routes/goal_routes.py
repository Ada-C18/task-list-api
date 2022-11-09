from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request
from .helpers_routes import validate_obj

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_obj(Goal, goal_id)

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
    goal = validate_obj(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    response = {
        "goal": goal.to_dict()
    }

    db.session.commit()

    return jsonify(response)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_obj(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
    }

    return jsonify(response)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_task_ids_to_goal(goal_id):
    goal = validate_obj(Goal, goal_id)

    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        # task = validate_task(task_id)
        task = validate_obj(Task, task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    response = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return response


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_obj(Goal, goal_id)

    tasks = goal.tasks
    tasks_list = [task.to_dict() for task in tasks]

    # convert goal to dict
    goal_dict = goal.to_dict()
    # add tasks_list to goal dict
    goal_dict["tasks"] = tasks_list

    # iterate tasks_list and add goal_id
    for task in goal_dict["tasks"]:
        task["goal_id"] = goal.goal_id

    return jsonify(goal_dict), 200
