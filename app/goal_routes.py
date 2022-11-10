from app import db
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from app.models.goal import Goal
from app.models.task import Task
import datetime
import os

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

def validate_goal(cls,id):
    try:
        id=int(id)
    except:
        abort(make_response(jsonify({"details": "Invalid data"}),400))
        
    goal = cls.query.get(id)

    if not goal:
        abort(make_response(jsonify({"details": "Invalid data"}), 404))

    return goal


@goal_bp.route("/", strict_slashes=False, methods =["GET"])
def read_all_goal():
    sort_by_title_query = request.args.get("sort")
    goals = ""
    goals_response = []
    if sort_by_title_query:
        if sort_by_title_query == "asc":
            goals = Goal.query.order_by(Goal.title.asc()).all()
        elif sort_by_title_query == "desc":
            goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
        # for goal in goals:
        #     goals_response.append(goal.to_dict())

    return jsonify(goals_response)


@goal_bp.route("/<id>", strict_slashes=False, methods =["GET"])
def read_one_goal(id):
    
    goal = validate_goal(Goal,id)
    return {"goal":goal.to_dict()}, 200

@goal_bp.route("/", strict_slashes=False, methods =["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except:

        return make_response(jsonify({"details": "Invalid data"}),400)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()},201


@goal_bp.route("/<id>", strict_slashes=False, methods =["PUT"])
def update_goal(id):

    goal = validate_goal(Goal,id)
    request_body = request.get_json()

    try:
        goal.title = request_body["title"]
    except:
        return make_response(jsonify({'warning':'Enter both title and description or use patch method'}),400)

    db.session.commit()
    return make_response(jsonify({"goal":goal.to_dict()}),200)


@goal_bp.route("/<id>", strict_slashes=False, methods =["DELETE"])
def delete_goal(id):

    goal = validate_goal(Goal,id)

    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f"{Goal.__name__} {goal.id} \"{goal.title}\" successfully deleted"
    }

    return make_response(jsonify(response_body),200)

@goal_bp.route("/<goal_id>/tasks", strict_slashes=False, methods =["GET"])
def read_tasks_goal(goal_id):
    
    goal = validate_goal(Goal,goal_id)

    return make_response(jsonify(goal.to_dict(tasks=True)), 200)

@goal_bp.route("/<goal_id>/tasks", strict_slashes=False, methods =["POST"])
def create_tasks_goal(goal_id):
    goal = validate_goal(Goal,goal_id)
    request_body = request.get_json()
    goal.tasks = [Task.query.get(task_id) for task_id in request_body["task_ids"]]

    db.session.commit()

    return make_response(jsonify(dict(id= goal.id, task_ids = [task.id for task in goal.tasks])),200)
