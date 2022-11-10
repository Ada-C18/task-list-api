from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime
from .task_routes import validate_model, wrap_response
import requests
import os


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


def validate_title(request_obj):
    obj_keys = request_obj.keys()
    if 'title' not in obj_keys:
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        return request_obj

@goals_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()
    request_body = validate_title(request_body)
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = wrap_response(Goal, new_goal.to_dict())

    return make_response(response_body, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify(wrap_response(Goal, goal.to_dict()))

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return jsonify(wrap_response(Goal, goal.to_dict()))

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": response_body})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_tasks_list(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    for task in request_body['task_ids']:
        new_task = validate_model(Task, task)
        goal.tasks.append(new_task)  
    db.session.commit()

    return jsonify({
        "id": int(goal_id),
        "task_ids": request_body['task_ids']
    })

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_all_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks_list = []
    for task in goal.tasks:
        if not task.completed_at:
            is_complete = False
        else:
            is_complete = True
        tasks_list.append(
            {
                "id": task.task_id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete
            }
        )
    return jsonify({
        "id": int(goal_id),
        "title": goal.title,
        "tasks": tasks_list
    })

