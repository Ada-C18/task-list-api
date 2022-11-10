from os import abort
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request 
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

goals_bp=Blueprint('goals_bp',__name__, url_prefix = '/goals')

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))

    return goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    # handles if title or description not included in post
    if "title" not in request_body:
        return make_response({"details":"Invalid data"},400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    goal_response = {"goal": new_goal.to_dict()}


    return make_response(jsonify(goal_response), 201)

@goals_bp.route("", methods=["GET"])
def return_all_goals():
    goals_response = []
    goals = Goal.query.all()


    sort_by_alpha_title_query = request.args.get("sort")

    if sort_by_alpha_title_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    if sort_by_alpha_title_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()

    for goal in goals:
        goals_response.append(goal.to_dict())
    return make_response(jsonify(goals_response),200)


# Gets one specific goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_response = {"goal": goal.to_dict()}
    return jsonify(goal_response), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goals(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    goal_response = {"goal": goal.to_dict()}


    return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    db.session.delete(goal)
    db.session.commit()
    return jsonify(goal_response), 200

# Returns tasks at specific goal
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_by_goal(goal_id):
    goal = validate_goal(goal_id)
    list_of_tasks = [task.to_dict() for task in goal.tasks]
    task_response = { "id": goal.goal_id, 
                    "title": goal.title,
                    "tasks": list_of_tasks}

    return jsonify(task_response), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_task(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    return_task_ids=[]
    for numbered_task in task_ids:
        current_task = Task.query.get(numbered_task)
        current_task.goal_id = goal.goal_id
        return_task_ids.append(int(numbered_task))
        db.session.commit()

    goal_response = {"id":int(goal_id),
        "task_ids":return_task_ids
        }

    return jsonify(goal_response), 200

