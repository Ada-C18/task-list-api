from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime

goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

"""Goal Routes Start"""
@goal_bp.route("", methods=['POST'])
def create_new_goal():
    response_body = request.get_json()
    
    try:
        new_goal = Goal(
            title=response_body["title"])
    except KeyError:
        return make_response({
        "details": "Invalid data"
    },400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({f"goal":new_goal.goal_dictionfy()}),201)

@goal_bp.route("", methods=['GET'])
def get_all_goals():
    return_list=[]
    
    sort_query = request.args.get("sort")
   
    goals = Goal.query.all()
    
    for goal in goals:
        return_list.append(goal.goal_dictionfy())
    
    return make_response(jsonify(return_list),200)

@goal_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return make_response(jsonify({"goal":goal.goal_dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['PUT'])
def update_one_goal(goal_id):
    response_body = request.get_json()
    goal = validate_model(Goal,goal_id)

    goal.title = response_body["title"]
   
    db.session.commit()

    return make_response(jsonify({f"goal":goal.goal_dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['DELETE'])
def delete_a_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response(jsonify({'details':f'Goal {goal_id} \"{goal.title}\" successfully deleted'}),200)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def create_book(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task,task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"]
    }), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = [task.dictionfy() for task in goal.tasks]
    return_dict = goal.goal_dictionfy()

    return_dict["tasks"] = task_list

    return make_response(jsonify(return_dict),200)

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model