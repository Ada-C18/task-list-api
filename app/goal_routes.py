from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app.models.goal import Goal
from app.routes import validate_model_id
from sqlalchemy import desc, asc
import datetime
import requests
import os
from app import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["GET"])
def retrieve_goals():
    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal.format_goal())
    return jsonify(goals_response)


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {"id": new_goal.goal_id, "title": new_goal.title}}, 201


@goals_bp.route("/<goal_id>", methods=["GET"])
def handle_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    return {"goal": goal.format_goal()}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return make_response({"goal": {"id": goal.goal_id, "title": goal.title}})


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(
        {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    )


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def add_task_to_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    tasks_response = []
    for task in Goal.query.get(goal_id).tasks:
        task.goal_id = goal.goal_id
        tasks_response.append(task.format_task_goal())

    return {"id": goal.goal_id, "title": goal.title, "tasks": tasks_response}


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def retrieve_tasks_from_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)
    request_body = request.get_json()
    task_ids = []
    for task_id in request_body["task_ids"]:
        task = validate_model_id(Task, task_id)
        task.goal_id = goal.goal_id
        task_ids.append(task.task_id)

    db.session.commit()

    return {"id": goal.goal_id, "task_ids": task_ids}
