from flask import Blueprint, jsonify, request
from app import db
from app.models.goal import Goal
from .routes_helper import validate_model
from app.models.task import Task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = Goal.to_dict(new_goal)

    return jsonify({"goal": goal_dict}), 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response = []

    for goal in goals:
        goal_dict = {
            "id": goal.goal_id,
            "title": goal.title
        }
        response.append(goal_dict)
    
    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    selected_goal = validate_model(Goal, goal_id)

    goal_dict = Goal.to_dict(selected_goal)

    return jsonify({"goal": goal_dict}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    selected_goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"message": "Request must include title and description"}), 400

    selected_goal.title = request_body["title"]

    db.session.commit()
    
    goal_dict = Goal.to_dict(selected_goal)
    return jsonify({"goal": goal_dict}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    selected_goal = validate_model(Goal, goal_id)

    db.session.delete(selected_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{selected_goal.title}" successfully deleted'}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_goal_ids_to_task(goal_id):
    selected_goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    
    for task_id in request_body["task_ids"]:
        valid_task = validate_model(Task, task_id)
        valid_task.goals = selected_goal
        db.session.commit()
    
    task_id_list = [task.task_id for task in selected_goal.tasks]
    
    response_body = {
        "id": selected_goal.goal_id,
        "task_ids": task_id_list
    }
    return jsonify(response_body), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    selected_goal = validate_model(Goal, goal_id)

    task_list = []
    for task in selected_goal.tasks:
        task_list.append(Task.to_dict(task))
    
    goal_dict = {
        "id": selected_goal.goal_id,
        "title": selected_goal.title,
        "tasks": task_list
    }

    return jsonify(goal_dict), 200