from app import db
from app.models.goal import Goal
from app.models.task import Task
from .taskroutes import validate_model
from flask import Blueprint, request, make_response, jsonify

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response)

@goals_bp.route("/<model_id>", methods=["GET"])
def read_one_goal(model_id):
    goal = validate_model(Goal, model_id)
    return {"goal":goal.to_dict()}, 200

@goals_bp.route("/<model_id>", methods=["PUT"])
def update_goal(model_id):
    goal = validate_model(Goal, model_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":goal.to_dict()}, 200

@goals_bp.route("/<model_id>", methods=["DELETE"])
def delete_goal(model_id):
    goal = validate_model(Goal, model_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

        db.session.commit()
        
    return make_response(jsonify({
        "id": goal.goal_id, "task_ids": request_body["task_ids"]
    })), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_one_goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = []
    for task in goal.tasks:
        tasks.append(task.task_with_goal_to_dict())
        
    return jsonify({
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks}), 200
