from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from .task_routes import validate_model
import requests
import os


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if (("title") not in request_body):
        return make_response({"details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    
    goal_response = Goal.query.get(1)
    return make_response({"goal": goal_response.to_dict()}, 201)

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()) #ColumnElement.desc() method produces a descending ORDER BY clause element
    else:
        goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return make_response({"goal": goal.to_dict()}, 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(
        {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}, 200
        )

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    
    task_list = []
    for id in task_ids:
        task = Task.query.get(id)
        task_list.append(task)
    goal.tasks = task_list

    db.session.commit()
    
    return make_response(
        {"id": goal.goal_id,
         "task_ids": task_ids},
        200
    )

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())
    
    return make_response(
        {"id": goal.goal_id,
         "title": goal.title,
         "tasks": tasks_response}
    )