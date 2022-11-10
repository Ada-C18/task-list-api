from app import db
from app.models.goal import Goal
from app.models.task import Task
from .task_routes import validate_model
from flask import Blueprint, jsonify, request, make_response, abort

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals_response = []
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    id_list = []
    if goal.tasks:
        for task in goal.tasks:
            id_list.append(task["task_id"])
    goal.to_dict()["task_id"] = id_list

    return make_response(jsonify({"goal": goal.to_dict()}), 200)

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_list_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        goal.tasks.append(Task.query.get(task_id)) 

    db.session.commit()

    return_body = {
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }

    return jsonify(return_body), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_list = []

    for task in goal.tasks:
        task_dict = task.to_dict()
        task_dict["goal_id"] = task.goal_id
        tasks_list.append(task_dict)

    return_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_list
    }

    return jsonify(return_body), 200
