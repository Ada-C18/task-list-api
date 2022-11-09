from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from ..models.goal import Goal
from ..models.task import Task
import datetime
import os

bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def validate_goal_dict(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False)):
        abort(make_response({'details': 'Invalid data'}, 400))

@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    validate_goal_dict(request_body)
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    

    return make_response({"goal": new_goal.to_dict()}, 201)

@bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")

    goal_query = Goal.query

    if sort_query:
        if sort_query == "desc":
            goal_query = goal_query.order_by(Goal.title.desc())
        else:
            goal_query = goal_query.order_by(Goal.title)

    goals = goal_query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = validate_model(Goal, id)
    return make_response({"goal": goal.to_dict()}, 200)

@bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)

@bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()
    return make_response({"details":f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, 200)

@bp.route("/<id>/tasks", methods=["POST"])
def create_task(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.tasks += [Task.query.get(task_id) for task_id in request_body["task_ids"]]

    db.session.commit()
    
    return make_response({"id": goal.id, "task_ids": [task.id for task in goal.tasks]}), 200