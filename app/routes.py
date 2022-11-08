from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import datetime
from .routes_helper import get_one_object_or_abort

import sys
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from dotenv import load_dotenv

task_bp = Blueprint("task_bp",__name__,url_prefix="/tasks")


@task_bp.route("",methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    if sort_param is None:
        tasks = Task.query.all()
    elif sort_param == "asc":
        tasks = Task.query.order_by("title")
    elif sort_param == "desc":
        tasks = Task.query.order_by(desc("title"))

    response = [task.to_dict() for task in tasks]

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>",methods=["GET"])
def get_task_by_id(task_id):
    task_with_id = get_one_object_or_abort(Task, task_id)

    response_body = {
        "task": {
            "id": task_with_id.task_id,
            "title": task_with_id.title,
            "description": task_with_id.description,
            "is_complete": task_with_id.is_complete
        }}

    return jsonify(response_body), 200
    
    # new_task = Task(
    #     title=request_body["title"],
    #     description=request_body["description"],
    # )
    # response_body = {
    #     "task": {
    #         "id": new_task.task_id,
    #         "title": new_task.title,
    #         "description": new_task.description,
    #         "is_complete": new_task.is_complete
    #         }
    #         }
@task_bp.route("",methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or \
    "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)
    response_body = {"task": new_task}

    db.session.add(new_task)
    db.session.commit()

    return jsonify(response_body), 201

@task_bp.route("/<task_id>",methods=["PUT"])
def update_task(task_id):
    selected_task = get_one_object_or_abort(Task, task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"message": "Request must include title and description"})
    
    selected_task.title = request_body["title"]
    selected_task.description = request_body["description"]

    db.session.commit()

    response_body = {
        "task": {
                "id": selected_task.task_id,
                "title": selected_task.title,
                "description": selected_task.description,
                "is_complete": selected_task.is_complete
                }}
    
    return jsonify(response_body), 200


@task_bp.route("/<task_id>",methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = get_one_object_or_abort(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f"Task {task_to_delete.task_id} \"{task_to_delete.title}\" successfully deleted"})

@task_bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def mark_task_complete(task_id):
    task_to_mark_complete = get_one_object_or_abort(Task, task_id)
    task_to_mark_complete.is_complete = True
    task_to_mark_complete.completed_at = datetime.today()

    db.session.commit()

    response_body = {
        "task": {
            "id": task_to_mark_complete.task_id,
            "title": task_to_mark_complete.title,
            "description": task_to_mark_complete.description,
            "is_complete": task_to_mark_complete.is_complete,
        }
    }

    client = WebClient(token=os.environ["SLACK_TOKEN"])
    logger = logging.getLogger(__name__)
    channel_id = "C04AJ78HYC8"
    result = client.chat_postMessage(
        channel=channel_id,
        text=f"Someone just completed the task {task_to_mark_complete.title}")

    return jsonify(response_body), 200

@task_bp.route("/<task_id>/mark_incomplete",methods=["PATCH"])
def mark_task_incomplete(task_id):
    task_to_mark_incomplete = get_one_object_or_abort(Task, task_id)
    task_to_mark_incomplete.is_complete = False
    task_to_mark_incomplete.completed_at = None

    response_body = {
        "task": {
            "id": task_to_mark_incomplete.task_id,
            "title": task_to_mark_incomplete.title,
            "description": task_to_mark_incomplete.description,
            "is_complete": task_to_mark_incomplete.is_complete
        }
    }

    db.session.commit()

    return jsonify(response_body), 200

"""GOAL ROUTES"""

goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

@goal_bp.route("",methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_goal = Goal.to_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    response_body = {"goal": new_goal}

    return response_body, 201
    

@goal_bp.route("",methods=["GET"])
def get_goals():
    goals = Goal.query.all()
    response = [goal.to_dict() for goal in goals]

    return jsonify(response), 200

@goal_bp.route("/<goal_id>",methods=["GET"])
def get_goal_by_id(goal_id):
    goal_with_id = get_one_object_or_abort(Goal, goal_id)

    response_body = {"goal": goal_with_id.to_dict()}

    return jsonify(response_body), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal_to_update = get_one_object_or_abort(Goal, goal_id)
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"})

    goal_to_update.title = request_body["title"]
    db.session.commit()
    response_body = {"goal": goal_to_update.to_dict()}

    return jsonify(response_body), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal_to_delete = get_one_object_or_abort(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_to_delete.goal_id} \"{goal_to_delete.title}\" successfully deleted"}), 200