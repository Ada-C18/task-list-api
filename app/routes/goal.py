import datetime
import os

import requests
from dotenv import load_dotenv
from flask import Blueprint, abort, jsonify, make_response, request

from app import db
from app.models.goal import Goal
from app.models.task import Task

bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {'message': f'{cls.__name__} {model_id} not found'}, 404))

    return model

def validate_title(cls, data):
    try:
        new_cls = cls(title = data["title"])
    except:
        abort(make_response(
            {"details": "Invalid data"}, 400))
    return new_cls



@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = validate_title(Goal,request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({
            "goal": {
            "id":new_goal.goal_id,
            "title": new_goal.title,
        }})
    , 201)

@bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    get_response = []

    for goal in goals:
        get_response.append(dict(
            id=goal.goal_id,
            title=goal.title
        ))
        
    return make_response(jsonify(get_response), 200)

@bp.route("/<goal_id>", methods=["GET"])
def handle_task(goal_id):

    goal = validate_model(Goal,goal_id)


    get_response ={
        f"goal": {
            "id": goal.goal_id,
            "title": goal.title
        }}

    return get_response, 200

@bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    update_response = {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
    }

    return make_response(update_response), 200

@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id, task_ids):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'
    })), 200


@bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal,goal_id)

    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.add(goal)
    db.session.commit()

    return make_response({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    }), 200

@bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    request_body = request.get_json
    goal = validate_model(Goal, goal_id)
    tasks = goal.tasks

    task_response = []

    for task in tasks:
        task =  {
            "id": task.task_id,
            "goal_id": goal.goal_id,
            "title": f"{task.title}",
            "description": f"{task.description}",
            "is_complete": bool(task.completed_at)
        }
        task_response.append(task)
    

    return make_response({
        "id": goal.goal_id,
        "title": f"{goal.title}",
        "tasks": task_response
    }), 200

@bp.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):

    task = validate_model(Task, task_id)

    return {
        "task": {
            "id": task_id,
            "goal_id": task.goal_id,
            "title": f"{task.title}",
            "description": f"{task.description}",
            "is_complete": bool(task.completed_at)
        }
    }

