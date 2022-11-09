from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import date
import os #newly added for wave4
import requests #newly added for wave4
from app.models.goal import Goal
from app import SLACK_URL
from app.routes.slack_bot import slack_message
from app.routes.task import get_all_objects, get_model_from_id, update_one_object

goal_bp = Blueprint("goal",__name__,url_prefix="/goals")
# task_bp = Blueprint("task", __name__, url_prefix="/tasks")



######################### WAVE 5 ##########################
@goal_bp.route('', methods=["GET"])
def get_all_goals():
    result = get_all_objects(Goal)
    return jsonify(result), 200

@goal_bp.route('/<goal_id>', methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_model_from_id(Goal,goal_id)
    return jsonify({"goal":chosen_goal.to_dict()}), 200

@goal_bp.route('', methods=["POST"])
def create_one_goal():
    request_body = request.get_json()    
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify({"details": "Invalid data"}),400
    
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_dict()}), 201

@goal_bp.route('/<goal_id>', methods=["PUT"])
def update_one_goal(goal_id):
    try:
        update_goal = update_one_object(Goal,goal_id)
    except KeyError:
        return jsonify({"details": "Invalid data"}),400
    
    db.session.commit()
    return jsonify({"goal":update_goal.to_dict()}),200

@goal_bp.route('/<goal_id>', methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete = get_model_from_id(Goal,goal_id)
    
    db.session.delete(goal_to_delete)
    db.session.commit()
    return jsonify({"details":f"Goal {goal_id} \"{goal_to_delete.title}\" successfully deleted"}), 200


@goal_bp.route('<goal_id>/tasks', methods=["POST"])
def create_task_id_to_goal(goal_id):
    goal = get_model_from_id(Goal,goal_id)
    request_body = request.get_json()

    task_list =[]
    for task_id in request_body["task_ids"]:
        task = get_model_from_id(Task, task_id)
        # if task:
        task.goal_id = goal.goal_id
        task_list.append(task.task_id)
    
    db.session.commit()

    return jsonify({"id":goal.goal_id, "task_ids": task_list}), 200

@goal_bp.route('<goal_id>/tasks', methods =["GET"])
def get_tasks_from_goal_id(goal_id):
    goal = get_model_from_id(Goal, goal_id)
    tasks = goal.get_task_list()
    
    return jsonify(goal.to_dict_task_id()), 200
    
