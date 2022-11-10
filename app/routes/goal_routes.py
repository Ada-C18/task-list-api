from flask import Blueprint,request,jsonify,abort, make_response
import requests, json
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import asc
from sqlalchemy import desc
from datetime import date
from app.routes.routes_helper import get_one_obj_or_abort
from app.routes.routes_helper import validate_id
from app.routes.task_routes import get_one_task_or_abort

goal_bp = Blueprint("goal_bp", __name__, url_prefix ="/goals")

@goal_bp.route("", methods=["POST"])
def create_Goal():
    request_body = request.get_json() 
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    goal_dict = new_goal.to_dict()

    return jsonify({"goal":goal_dict}), 201

@goal_bp.route("", methods = ["GET"])
def get_Goal_all():
    goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods =["GET"])
def get_one_Goal(goal_id):
    validate_id(goal_id, 'goal_id')
    goal = get_one_obj_or_abort(Goal,goal_id)
    if not goal:
        response_str = f"Could not find goal with ID {goal_id}"
        abort(make_response(jsonify({"message": response_str}),404))
    goal_dict = goal.to_dict()
    return jsonify({"goal": goal_dict}), 200
    

@goal_bp.route("/<goal_id>", methods = ["PUT"])
def update_Goal(goal_id):
    validate_id(goal_id, 'goal_id')
    goal = get_one_obj_or_abort(Goal, goal_id)
    if not goal:
        response_str = f"Goal with id {goal_id} not found in database"
        abort(make_response(jsonify({"message": response_str}),404))
    request_body = request.get_json() #converts json into dictionary
    goal.title = request_body["title"]
    db.session.commit()
    goal_dict = goal.to_dict()
    return jsonify({"goal":goal_dict}), 200

@goal_bp.route("<goal_id>", methods=["DELETE"])
def delete_one_Goal(goal_id):
    validate_id(goal_id, 'goal_id')
    chosen_goal = get_one_obj_or_abort(Goal, goal_id)
    if not chosen_goal:
        response_str = f"Goal with id {goal_id} not found in database"
        abort(make_response(jsonify({"message": response_str}),404))

    db.session.delete(chosen_goal)
    db.session.commit()
    return jsonify({"details": f'Goal {goal_id} "Build a habit of going outside daily" successfully deleted'}),200


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def update_task(goal_id):
    validate_id(goal_id, 'goal_id')
    goal = get_one_obj_or_abort(Goal, goal_id)
    if not goal:
        response_str = f"Goal with id {goal_id} not found in database"
        abort(make_response(jsonify({"message": response_str}),404))
    request_body = request.get_json() 
    task_id_list = request_body["task_ids"] 
    for task_id in task_id_list:
        task_obj=get_one_obj_or_abort(Task, task_id)
        task_obj.goal=goal
        db.session.commit()
    goal_dict = {"id": goal.goal_id,
    "task_ids": task_id_list
    }
    return make_response(jsonify(goal_dict)),200

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = [goal.to_dict() for goal in goals]
    return jsonify(response), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_belonging_to_a_goal(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)
    if goal is None:
        response_str = f"id {goal_id} was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))

    task_response = [task.to_dict() for task in goal.tasks]
    goal_dict = goal.to_dict()
    goal_dict["tasks"] = task_response
    return jsonify(goal_dict),200