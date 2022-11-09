from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.goal import Goal
from datetime import date
from app.models.task import Task


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("",methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_goal = Goal(
            title=request_body["title"],
            )
    except:
        return jsonify({
        "details": "Invalid data"
    }), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify(new_goal.to_dict_goal()), 201

@goal_bp.route("",methods=["GET"])
def get_all_goals():
    title_query_value = request.args.get("title")
    ascending_order = request.args.get("sort")
    
    goals = Goal.query 
    
    if title_query_value is not None:
        goals = goals.filter_by(title=title_query_value)
    if ascending_order == "asc":
        goals = goals.order_by(Goal.title.asc())
    if ascending_order == "desc":
        goals = goals.order_by(Goal.title.desc())

    result = []
    for goal in goals.all():
        result.append(goal.to_dict_all_goals())
    return jsonify(result), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_goal_from_id(goal_id)
    return jsonify(chosen_goal.to_dict_goal()), 200

def get_goal_from_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"message":f"Invalid data type {goal_id}"}, 400))

    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        return abort(make_response({"message": f"Could not find a goal with id {goal_id}"}, 404))

    return chosen_goal

@goal_bp.route("/<goal_id>",methods=["PUT"])
def update_one_goal_id(goal_id):
    update_goal = get_goal_from_id(goal_id)
    request_body = request.get_json()

    try:
        update_goal.title = request_body["title"]
    except KeyError:
        return jsonify({"details":f"Invalid data"}), 400

    db.session.commit()
    return jsonify(update_goal.to_dict_goal()), 200

@goal_bp.route("/<goal_id>",methods=["DELETE"])
def delete_one_goal(goal_id):
    goal_to_delete=get_goal_from_id(goal_id)
    
    db.session.delete(goal_to_delete)
    db.session.commit()
    
    return jsonify({"details":f'Goal {goal_to_delete.goal_id} "{goal_to_delete.title}" successfully deleted'}), 200

@goal_bp.route('/<goal_id>/tasks', methods=['POST'])
def get_all_tasks_for_goal(goal_id):
    goal = get_goal_from_id(goal_id) # goal is a full goal - only 1 goal

    request_body = request.get_json() # request_body is dictionary

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id) # task_id only to retrieve the whole task
        goal.tasks.append(task)

    id_list = []
    for task in goal.tasks:
        if task.task_id not in id_list:
            id_list.append(task.task_id)

    db.session.commit()

    return jsonify({"id":goal.goal_id, "task_ids": id_list}), 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_one_goal(goal_id):
    goal = get_goal_from_id(goal_id)

    task_list = []
    for task in goal.tasks:
        task_list.append(Task.to_dict_all_tasks_with_goal(task))

    return jsonify({"id": goal.goal_id, "title": goal.title, "tasks": task_list}), 200

