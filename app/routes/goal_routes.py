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

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
            "goal": new_goal.to_dict_goal()
        }, 201


@bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    print(request_body)

    db.session.commit()

    return make_response(jsonify(f"Updated Goal Title"))


@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal:

        goal_dict = {
        "details": f"Goal {goal_id} \"{goal.title }\" successfully deleted"}

        db.session.delete(goal)
        db.session.commit()
        return jsonify(goal_dict), 200
    else:
        response_body = {
            "details": f"Goal {goal_id} \"{goal.title }\" was not found"
        }, 404
    

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

    task_ids = request_body["task_ids"]

    for task in task_ids:
        task = validate_model(Task, task)
        task.goal= goal
        if task not in goal.tasks:

            goal.tasks.append(task) # Changed from id to goal_id
            db.session.add(goal)
            db.session.commit()
    db.session.add(goal)
    db.session.commit()

    response = {
                "id": int(goal_id),
                "task_ids": task_ids 
            }

    return make_response(jsonify(response), 200)   

@bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_tasks_of_one_goal(goal_id):
    goal=validate_model(Goal, goal_id)
    
    list_of_tasks    = []

    for task in goal.tasks:
        list_of_tasks.append(Task.to_dict(task))

    goal_dict = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks" : list_of_tasks
    }

    return jsonify(goal_dict), 200



    # task_list = []
    # for task in goal.tasks:
    #     task_list.append(task.to_dict_goal())

    # return make_response({"id": goal.goal_id, "title": goal.title, "tasks": task_list})
    
    # if goal:
    #     goal_dict = {"goal_id" :
    #     {
    #     "goal_id": goal_id,
    #     "title": goal.title,
    #     "tasks": [],
    #     }}

    # for task in goal.Tasks:
    #     goal_dict["tasks"].append(task.to_dict_())
    
    # # return goal_dict, 200
    # return make_response({"id": goal.goal_id, "title": goal.title, "tasks": {goal__dict})
        
    # tasks_list_of_dicts = []

    # for task in goal.tasks:
    #     task_dict = {}
    #     task_dict["id"] = task.task_id
    #     task_dict["goal_id"] = task.goal_id
    #     task_dict["title"] = task.title
    #     task_dict["description"] = task.description
    #     task_dict["is_complete"] = False
    #     tasks_list_of_dicts.append(task_dict)

    # return {
    #     "id": goal.goal_id,
    #     "title": goal.title,
    #     "tasks": tasks_list_of_dicts
    # }
    