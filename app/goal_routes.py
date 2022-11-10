
from datetime import datetime
from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc #(used in read_all_tasks for sorting)
import os 
from .task_routes import validate_model

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

#CREATE Routes (Wave 5: CRUD Routes for goal model)

@goals_bp.route('', methods=['POST'])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return jsonify ({"details": "Invalid data"}), 400
    
    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route('', methods=["GET"])
def get_all_goals():
    all_goals = Goal.query.all()

    result = [item.to_dict() for item in all_goals]

    return jsonify(result), 200

@goals_bp.route("<goal_id>", methods=["GET"])
def read_goal_by_id(goal_id): 
    chosen_goal = validate_model(Goal, goal_id)
    
    return jsonify({"goal": chosen_goal.to_dict()}), 200

@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    update_goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    try:
        update_goal.title = request_body["title"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400
    
    db.session.commit()
    return jsonify({"msg": f"Successfully updated goal with id {update_goal.goal_id}"}), 200

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal_to_delete = validate_model(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'}), 200

#Wave 6: Nested Routes
@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def add_task_ids_to_goal(goal_id):
    chosen_goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for id in task_ids:
        #task = Task.query.get(int(id))
        task = validate_model(Task, int(id))
        if task not in chosen_goal.tasks:
            chosen_goal.tasks.append(task)
            #db.session.add(task)
            db.session.commit()
    
    return jsonify({
        "id" : int(goal_id),
        "task_ids": task_ids
    }), 200

@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def get_tasks_by_goal_id(goal_id):
    chosen_goal = validate_model(Goal, goal_id)

    return jsonify(chosen_goal.to_dict_incl_tasks()), 200
    
    




        

