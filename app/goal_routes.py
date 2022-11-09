from flask import Blueprint, request, jsonify, make_response, abort
from app import db 
from app.models.task import Task
from app.models.goal import Goal
from datetime import date
import logging
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from app.routes import validate_model_id

goals_bp = Blueprint("goals", __name__, url_prefix = "/goals")

#CREATE a new goal
@goals_bp.route("", methods = ["POST"])
def create_new_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal.to_dict()}

    return jsonify(response_body), 201

#READ all goals
@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response = [goal.to_dict() for goal in goals]

    return jsonify(response), 200

#GET get one goal
@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):

    goal = validate_model_id(Goal, goal_id)

    response_body = {"goal": goal.to_dict()}

    return jsonify(response_body), 200
    
#UPDATE goal
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return jsonify(response_body), 200

#DELETE a goal
@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200


# POST assign tasks to a goal 
@goals_bp.route("/<goal_id>/tasks", methods = ["POST"])
def post_task_ids_to_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    request_body = request.get_json()
    task_id_list = request_body.get("task_ids")

    for task_id in task_id_list:
        task = validate_model_id(Task, task_id)
        goal.tasks.append(task)
        task.goal_id = goal_id

    db.session.commit()
    response_body = {"id": goal.goal_id, "task_ids": task_id_list}

    return jsonify(response_body), 200

# GET tasks of one goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    tasks = goal.get_task_list()

    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks
    } 
    return jsonify(response_body), 200