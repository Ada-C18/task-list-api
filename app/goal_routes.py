import json
import datetime
from os import abort

from flask import Blueprint, abort, jsonify, make_response, request
from sqlalchemy import asc, desc

from app import db
from app.models.goal import Goal
from app.models.task import Task

goals_bp = Blueprint('goals', __name__, url_prefix="/goals")


def validate_goal_id(cls, goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {goal_id} invalid"},400))

    goal = cls.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"{cls.__name__} {goal_id} not found"}, 404))

    return goal


@goals_bp.route('/<goal_id>', methods=['GET'])
def no_saved_goal(goal_id):
    goal_validate = validate_goal_id(goal_id)
    
    goal_response = []
    # goal.todict() for goal in Goal

    if goal_response is None:
        return "The goal ID submitted, does not exist: error code 404"
    else:    
        return jsonify({goal_validate.goal_dict()}),200 

@goals_bp.route('/<goal_id>', methods=['GET'])
def one_saved_goal(goal_id):
    goal_validate = validate_goal_id(goal_id)
    
    goal_response = [goal.todict() for goal in Goal]

    if goal_id == None:
        return "The goal ID submitted, does not exist: error code 404"
    else:    
        return jsonify({goal_validate.goal_dict()}), 


@goals_bp.route('/<goal_id>', methods=['GET'])
def get_goal():
    goal_validate = validate_goal_id()
    
    goal_response = [goal.todict() for goal in Goal]

    if goal_validate == None:
        return "The goal ID submitted, does not exist: error code 404"
    else:    
        return jsonify({"goal": goal_validate.goal_dict()}), 200

@goals_bp.route("", methods=['POST'])
def create_goal():
    response_body = request.get_json()

    if "title" not in response_body:
        return jsonify({"details": "Invalid data"}), 400
    
    created_goal = Goal(title=response_body["title"])

    # new_goal.goal = Goal

    db.session.add(created_goal)
    db.session.commit()
    
    return jsonify({"goal": created_goal.goal_dict()}), 201


@goals_bp.route("/<goal_id>/tasks", methods=['GET'])
def goal_not_found(goal_id):
    response_body = request.get_json()
    print(response_body)

    goal = validate_goal_id

    if not goal:
        return "The goal ID submitted, does not exist: error code 404"
    else:    
        return jsonify({"goal": goal.goal_dict()}), 200
    
    # return make_response(jsonify({"goal": created_goal.goal_dict()}))

@goals_bp.route('', methods=['GET'])
def query_all():
    
    sort_query = request.args.get("sort")
    
    query_lists = []
    
    if sort_query== "desc":
        query_goals = Goal.query.order_by(Goal.title.desc())


    elif sort_query == "asc":
        query_goals = Goal.query.order_by(Goal.title.asc())

    else:
        query_goals = Goal.query.all()

    for query in query_goals:
        query_lists.append(query.goal_dict())

    return jsonify(query_lists), 200



@goals_bp.route('/<goal_id>', methods=['PUT'])
def update_goals(goal_id):
    
    validate_id = validate_goal_id(goal_id)

    response_body = request.get_json()
    
    validate_id.title = response_body["title"]
    validate_id.description = response_body["description"]


    db.session.commit()

    return jsonify({"goal": validate_id.goal_dict()}),200
    

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goals(goal_id):
    test_goal = validate_goal_id(goal_id)
    result_notice = {"details": f'Goal {goal_id} "{test_goal.title}" successfully deleted'}

    db.session.delete(test_goal)
    db.session.commit()

    return make_response(result_notice, 200)
