
import os
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, abort, jsonify, make_response, request
import requests
from app.routes import validate_task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        return abort(make_response({"message": f"goal {goal_id} has an invalid goal_id"}), 400)

    query_result = Goal.query.get(goal_id)

    if not query_result:
        abort(make_response({"message": f"goal {goal_id} not found"}, 404))

    return query_result

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_goal = Goal(title=request_body["title"])
    
    
    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": Goal.to_dict(new_goal)})), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def one_saved_goal(goal_id):
    goal = validate_id(goal_id)
    
    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goal_list = []
    for goal in goals:
        goal_list.append(goal.to_dict())
    
    return jsonify(goal_list)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted" })), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_id(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()

    return make_response(jsonify({"goal": Goal.to_dict(goal)})), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def task_to_goal(goal_id):
    goal = validate_id(goal_id)
    
    request_body = request.get_json()
    task_ids= []
    for task_id in request_body["task_ids"]:
        task = validate_task(task_id)
        task.goal_id= goal.goal_id
        task_ids.append(task_id)

    db.session.commit()
    
    return jsonify({
        "id":task.goal_id,
        "task_ids":task_ids
    }), 200
    

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_includes_id(goal_id):
    goal = validate_id(goal_id)
    
    goals_list = []
    for task in goal.tasks:
        goals_list.append(Task.to_dict(task))
    
    return jsonify({
        "id": goal.goal_id,
        "title":goal.title,
        "tasks":goals_list
    })
    