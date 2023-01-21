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


# @goals_bp.route('/<goal_id>', methods=['GET'])
# def no_saved_goal(goal_id):
#     goal_validate = validate_goal_id(goal_id)
    
#     goal_response = []
#     # goal.todict() for goal in Goal

#     if goal_response is None:
#         return None
#     else:    
#         return jsonify({goal_validate.goal_dict()}),200 

# @goals_bp.route('/<goal_id>', methods=['GET'])
# def one_saved_goal(goal_id):
#     goal_validate = validate_goal_id(goal_id)
    
#     goal_response = [goal.todict() for goal in Goal]

#     if goal_id == None:
#         return None
#     else:    
#         return jsonify({goal_validate.goal_dict()}), 

@goals_bp.route('/<goal_id>', methods=['GET'])
def get_goal(goal_id):
    goal_validate = validate_goal_id(Goal,goal_id)

    
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
    
    goal_object = validate_goal_id(Goal,goal_id)

    response_body = request.get_json()
    
    if "title" in response_body:
        goal_object.title = response_body["title"]

    db.session.commit()

    return jsonify(goal_object.goal_dict()), 200
    

@goals_bp.route('/<goal_id>', methods=['DELETE'])
def delete_goals(goal_id):
    test_goal = validate_goal_id(Goal,goal_id)
    result_notice = {"details": f'Goal {goal_id} "{test_goal.title}" successfully deleted'}

    db.session.delete(test_goal)
    db.session.commit()

    return make_response(result_notice, 200)

@goals_bp.route('/<goal_id>/tasks', methods=['POST'])
def task_ids_to_goal(goal_id):
    goal_object = validate_goal_id(Goal,goal_id)

    request_body = request.get_json()

    goal_object.tasks = [Task.query.get(task_id) for task_id in request_body["task_ids"]]
    db.session.commit()
    
    return {"id":goal_object.goal_id,
            "task_ids":[task.task_id for task in goal_object.tasks]}, 200


@goals_bp.route('/<goal_id>/tasks', methods=['GET'])
def goal_with_no_task(goal_id):
    goal_object = validate_goal_id(Goal,goal_id)

    # request_body = request.get_json()

    tasks = [task.build_task_dict() for task in goal_object.tasks] 
    
    return {"id": goal_object.goal_id, "title": goal_object.title,
            "tasks": tasks}, 200
