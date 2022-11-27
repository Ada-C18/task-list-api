from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify, make_response, abort
from sqlalchemy import desc
from datetime import datetime
import requests
import os
from .validate_model import validate_model


bp = Blueprint("bp", __name__, url_prefix="/goals")

@bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()

    goals_list = [goal.to_dict_goal() for goal in goals]
        
    return make_response(jsonify(goals_list), 200)

@bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal:
        return {
            "goal": goal.to_dict_goal()}, 200  
    else:
        response_body = {
            "details": "Invalid data"} 
        return make_response(jsonify(response_body)) 
   
@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400


    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({
            "goal": new_goal.to_dict_goal()
        }), 201


@bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    request_body = request.get_json()

    if "title" in request_body:
        goal.title = request_body["title"]
    db.session.commit()
    response_body = {
        "goal": goal.to_dict_goal()
    }
    return make_response(jsonify(response_body, 200))

@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal:

        goal_dict = {
        "details": f"Goal {goal_id} \"{goal.title }\" successfully deleted"}

        db.session.delete(goal)
        db.session.commit()
        return jsonify(goal_dict), 200
    

@bp.route("/<goal_id>/tasks", methods=["GET"])
def goal_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    
    goal_dict = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": []
    }

    for task in goal.tasks:
        goal_dict["tasks"].append(task.to_dict())

    return jsonify(goal_dict), 200

@bp.route("/<goal_id>/tasks", methods=["POST"])
def sending_list_of_task_ids_to_goal(goal_id):
    goal= validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.tasks = []
    
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

        db.session.commit()

    response = {
                "id": goal.goal_id,
                "task_ids": request_body["task_ids"]
            }

    return make_response(jsonify(response), 200)   

@bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_tasks_of_one_goal(goal_id):
    goal=validate_model(Goal, goal_id)

    goals_list = [goal.to_dict_goal() for goal in goal.tasks]

    return jsonify(goals_list), 200