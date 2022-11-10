from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from sqlalchemy import asc, desc
import datetime, requests, os
from dotenv import load_dotenv
from .taskroutes import validate_model


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals_response = []
    goals = Goal.query.all()
    
    for goal in goals:
        goals_response.append(goal.goal_dict())
    
    return jsonify(goals_response) 
    

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.goal_dict()}, 200


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({
            "details": "Invalid data"}), 400
    
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": new_goal.goal_dict()}, 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    return {"goal": goal.goal_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        goal.tasks.append(task) 
    
        db.session.commit()
    
    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids": request_body["task_ids"]
    })), 200
    
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_task_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks_response = []
    for task in goal.tasks:
        tasks_response.append({
                "id": task.task_id,
                "goal_id": goal.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
                
            }), 200
    return jsonify({
                "id": goal.goal_id,
                "title": goal.title,
                "tasks": tasks_response}), 200
