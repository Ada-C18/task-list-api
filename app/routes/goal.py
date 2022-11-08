from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal
from datetime import datetime
from app.models.task import Task
from .task import get_one_task_or_abort
import requests
import os

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()
    return make_response(jsonify({"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }}), 201)


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append({
            "id": goal.goal_id,
            "title": goal.title,

        })
    return make_response(jsonify(response), 200)


def get_one_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({'msg': f'Invalid id: {goal_id}.ID must be an integer '}, 400))

    matching_goal = Goal.query.get(goal_id)
    if matching_goal is None:
        return abort(make_response({'msg': f'could not find task item with id: {goal_id}'}, 404))

    return matching_goal


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)

    return make_response(jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,
    }}), 200)


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_with_new_vals(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"msg": "Request must include title, description"}), 400

    chosen_goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal": {
        "id": chosen_goal.goal_id,
        "title": chosen_goal.title,
    }}), 200)


@ goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)
    db.session.delete(chosen_goal)
    db.session.commit()
    return make_response({'details': f'Goal {chosen_goal.goal_id} "{chosen_goal.title}" successfully deleted'}), 200


# adding AND geting list of tasks
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = get_one_goal_or_abort(goal_id)
    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = get_one_task_or_abort(task_id)
        task.goal_id = int(goal_id)
        db.session.add(task)
        db.session.commit()
    return jsonify({"id": goal.goal_id, "task_ids": request_body["task_ids"]}), 200


# get goal tasks using <goal_id>/tasks
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_goal_tasks(goal_id):
    chosen_goal = get_one_goal_or_abort(goal_id)
    tasks_list = []
    for task in chosen_goal.tasks:
        tasks_list.append(task.to_dict())
    goal_dict = chosen_goal.to_dict()
    return jsonify(goal_dict), 200


# validateing goal and using as a helper function

def get_one_goal_or_abort(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({'msg': f'Invalid id": "ID must be an integer '}, 400))

    matching_goal = Goal.query.get(goal_id)
    if matching_goal is None:
        return abort(make_response({"msg": f"could not find goal item with id"}, 404))

    return matching_goal
