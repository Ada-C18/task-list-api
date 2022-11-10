from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.task_routes import validate_model
from datetime import date

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}), 201


@goal_bp.route('', methods=['GET'])
def get_or_sort_goals():
    goals = Goal.query.all() 
    result = []
    for goal in goals:
        result.append(goal.to_dict())
    
    return jsonify(result), 200


@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal_chosen = validate_model(Goal, goal_id)

    return jsonify({"goal":goal_chosen.to_dict()}), 200


@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    update_goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    update_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": update_goal.to_dict()}), 200


@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    delete_goal = validate_model(Goal, goal_id)

    db.session.delete(delete_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{delete_goal.title}" successfully deleted'}), 200


@goal_bp.route('/<goal_id>/tasks', methods=['POST'])
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    for id in request_body["task_ids"]:
        new_task = validate_model(Task, id)
        new_task.goal = goal
        db.session.add(new_task)
        db.session.commit()
    
    return jsonify({"id": int(goal_id),
                   "task_ids": request_body["task_ids"]})


@goal_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_task_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_result = [] 
    for task in goal.tasks:
        tasks_result.append(task.to_dict_nested())
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks_result
    }), 200
