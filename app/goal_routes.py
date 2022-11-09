from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from .routes import *
from app import db

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    
    request_body = request.get_json()

    if not "title" in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"]
        )

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response({"goal": new_goal.to_json()},201)

@goal_bp.route("", methods=["GET"])
def get_goal_list():

    sort_query = request.args.get("sort")
    goal_query = Goal.query

    if sort_query:
        goal_query = goal_query.order_by(Goal.title)

    goals = goal_query.all()

    goals_list = [goal.to_json() for goal in goals]

    return jsonify(goals_list)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    return make_response({"goal":goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goals(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    return make_response({"goal": goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)

    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    
    goal_id = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal_id.tasks = [Task.query.get(id) for id in request_body["task_ids"]]

    db.session.commit()
    
    return {
        "id": goal_id.goal_id,
        "task_ids": request_body["task_ids"],
    }

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_goals(goal_id):
    
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_json()

    if goal.tasks:
            tasks_dict = [task.to_dict() for task in goal.tasks]
            goal_dict["tasks"] = tasks_dict

    else:
        goal_dict["tasks"] = []

    return jsonify(goal_dict)



