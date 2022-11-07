from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app.helper_functions import validate_model, post_one_model, get_one_model, get_all_models, delete_one_model
from app import db

goal_bp = Blueprint("goal_bp",__name__,url_prefix="/goals")

"""Goal Routes Start"""
@goal_bp.route("", methods=['POST'])
def create_new_goal():
    return post_one_model(Goal)

@goal_bp.route("", methods=['GET'])
def get_all_goals():
    return get_all_models(Goal)

@goal_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    return get_one_model(Goal,goal_id)

@goal_bp.route("/<goal_id>", methods=['PUT','PATCH'])
def update_one_goal(goal_id):
    response_body = request.get_json()
    goal = validate_model(Goal,goal_id)
    try:
        goal.title = response_body["title"]
    except KeyError:
        return make_response(jsonify({'warning':'Enter a title'}),400)

    db.session.commit()

    return make_response(jsonify({f"goal":goal.dictionfy()}),200)

@goal_bp.route("/<goal_id>", methods=['DELETE'])
def delete_a_goal(goal_id):
    return delete_one_model(Goal,goal_id)

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def map_tasks_to_goals(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    for task_id in request_body["task_ids"]:
        task = validate_model(Task,task_id)
        task.goal_id = goal.goal_id

    db.session.commit()

    return make_response(jsonify({
        "id": goal.goal_id,
        "task_ids":request_body["task_ids"] #this works because it'll throw an abort error if not all are added
    }), 200)


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = [task.dictionfy() for task in goal.tasks]
    return_dict = goal.dictionfy()

    return_dict["tasks"] = task_list

    return make_response(jsonify(return_dict),200)
