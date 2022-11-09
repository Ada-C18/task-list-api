from flask import Blueprint
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .task_routes import validate_model
from flask import Blueprint, jsonify, make_response, request, abort
import datetime as dt

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#CREATE goal
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    try:
        new_goal = Goal.from_dict_to_instance(request_body)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.from_instance_to_dict()},201


# GET all goals
@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.from_instance_to_dict())

    return jsonify(goals_response)


# GET one goal
@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal":goal.from_instance_to_dict()}


#UPDATE one goal
@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":goal.from_instance_to_dict()}

# DELETE goal
@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# POST list of task IDs to a Goal /goals/<goal_id>/tasks
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_goal_with_tasks(goal_id):

    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    
    task_list = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task.goal = goal 
        task_list.append(task_id)

    db.session.commit()
    return jsonify({"id": goal.goal_id, "task_ids": task_list}), 200

# GET all tasks for specific Goal id
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_dict = goal.from_instance_to_dict(tasks = True)
    return goal_dict

