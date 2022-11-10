from os import abort
import os
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from requests import post
from datetime import datetime, timezone

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_model(class_obj, object_id):
    try:
        object_id = int(object_id)
    except:
        abort(make_response(jsonify({"message": f"Goal {object_id} has an invalid goal_id"}), 400))

    query_result = class_obj.query.get(object_id)

    if not query_result:
        abort(make_response({"message": f"Goal {object_id} not found"}, 404))

    return query_result

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]

    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        goals_response = sorted(goals_response, key=lambda dict: dict["title"])
    elif sorting_query == "desc":
        goals_response = sorted(goals_response, key=lambda dict: dict["title"], reverse=True) 

    return jsonify(goals_response), 200
    
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    print(request_body)
    if "title" in request_body:
        new_goal = Goal.from_dict(request_body)
        db.session.add(new_goal)
        db.session.commit()
        response_one_goal = {}
        response_one_goal["goal"] = Goal.to_dict(new_goal)
        return jsonify(response_one_goal), 201
    else:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_one_goal = {"goal": Goal.to_dict(goal)}
    return jsonify(response_one_goal), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.update(request_body)

    goal.title = request_body["title"]

    db.session.commit()
    response_updated_goal = {"goal": Goal.to_dict(goal)}
    return jsonify(response_updated_goal), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    for task_id in request_body["task_ids"]:
        valid_task = validate_model(Task, task_id)
        valid_task.goal = goal

    db.session.commit()

    return make_response(jsonify({"id": goal.id, "task_ids": [task.id for task in goal.tasks]}), 200)

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):

    goal = validate_model(Goal, goal_id)

    tasks_response = [{"id": task.id, 
                        "title": task.title, 
                        "description": task.description, 
                        "goal_id": task.goal_id, 
                        "is_complete": task.is_complete} 
                    for task in goal.tasks]

    return make_response(jsonify({"id": goal.id, "title": goal.title, "tasks": tasks_response}), 200)