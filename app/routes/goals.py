
from app import db
from datetime import date
from app.models.task import Task
from app.models.goal import Goal
from .routes_helper import get_one_task_or_abort
from .routes_helper import get_one_goal_or_abort
from flask import Blueprint, jsonify, make_response, request, abort
import requests, os


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>G O A L S<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def add_one_goal():
    
    request_body = request.get_json()
    
    if "title" not in request_body:
        return jsonify({"details":"Invalid data"}), 400

    new_goal = Goal (
        title=request_body["title"]
    )
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    
    goals = Goal.query.all()
    
    response = []
    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@goal_bp.route("<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    
    selected_goal = get_one_goal_or_abort(goal_id)
    
    return jsonify({"goal" : selected_goal.to_dict()}), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):

    selected_goal= get_one_goal_or_abort(goal_id)

    request_body = request.get_json()

    if "title" not in request_body:

            return jsonify({"message":"Request must include title."}), 400

    selected_goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal" : selected_goal.to_dict()}), 200


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    selected_goal= get_one_goal_or_abort(goal_id)
    
    db.session.delete(selected_goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{selected_goal.title}" successfully deleted'}), 200


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>RELATIONSHIP<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_on_goal(goal_id):

    validate_goal_id = get_one_goal_or_abort(goal_id)

    request_body = request.get_json()
    
    for id in request_body["task_ids"]:
        new_task = Task.query.get(id)
        validate_goal_id.tasks.append(new_task)

    db.session.commit()

    return jsonify({"id": validate_goal_id.goal_id, "task_ids": [task.task_id for task in validate_goal_id.tasks]}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_tasks(goal_id):
    validate_goal_id = get_one_goal_or_abort(goal_id)

    if not validate_goal_id:
        return make_response("", 404)

    return jsonify({"id": validate_goal_id.goal_id, "title":validate_goal_id.title, "tasks":[task.to_dict() for task in validate_goal_id.tasks]}), 200