from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify, make_response, abort
from sqlalchemy import desc
from datetime import datetime
import requests
import os


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# goals
@goals_bp.route("", methods=["POST", "GET"])
def handle_goals():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body:
            return jsonify(details="Invalid data"), 400

        new_goal = Goal(
            title=request_body["title"]
        )

        db.session.add(new_goal)
        db.session.commit()
        return jsonify(goal=new_goal.to_json_goal()), 201

    elif request.method == "GET":
        goals = Goal.query.all()
        response_body = []
        for goal in goals:
            response_body.append(goal.to_json_goal())

        return jsonify(response_body), 200


@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_Goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == "GET":
        return jsonify(goal=goal.to_json_goal()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        goal.title = request_body["title"]
        db.session.commit()
        return jsonify(goal=goal.to_json_goal()), 200

    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return jsonify(details="Goal 1 \"Build a habit of going outside daily\" successfully deleted"), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def handle_goals_tasks(goal_id):
    goal = Goal.query.get_or_404(goal_id)

    if request.method == "POST":
        request_body = request.get_json()
        task_list = request_body["task_ids"]

        for task_id in task_list:
            task = Task.query.get(task_id)
            task.goal = goal

        db.session.commit()
        return {
            "goal_id": goal.goal_id,
            "task_ids": task_list
        }, 200

    elif request.method == "GET":
        tasks = goal.tasks
        task_response = []
        for task in tasks:
            task_response.append(task.to_json_task())

        return {
            "goal_id":  goal.goal_id,
            "title": goal.title,
            "tasks": task_response
        }, 200


@goals_bp.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": 404, "message": "Not found"}),404

@goals_bp.errorhandler(400)
def bad_request(error):
    return jsonify({"success": False, "error": 400, "message": "Bad request"}),400

@goals_bp.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}),422


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    request_body = request.get_json()
    if not request_body: 
        abort(400)
    elif "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    response_body = {
        "goal": goal.to_dict()
    }
    return make_response(response_body, 200)

def get_goal_by_id(goal_id):
    valid_int(goal_id, "goal_id")
    return Goal.query.get_or_404(goal_id, description='{Goal not found}')
def valid_int(number, parameter_type):
    try:
        int(number)
    except:
        abort(make_response({"error": f'{parameter_type} must be an integer'}, 400))


