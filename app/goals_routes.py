from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.routes import get_task_from_id



goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#helper function to get goal by id: 
def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"msg":f"Invalid data type: {goal_id}"}, 400))
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        return abort(make_response({"msg": f"Could not find goal item with id: {goal_id}"}, 404))
    return chosen_goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify(
            {"details": "Invalid data"}), 400
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}),201

@goals_bp.route("", methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    return jsonify({
        "goal": goal.to_dict()
    })

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_goal_id(goal_id)

    if "title" not in request_body:
        return jsonify({"msg": "Request must include a title"}),400
    goal.title = request_body["title"]
    db.session.commit()
    return jsonify({
        "goal": goal.to_dict()
    })

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        })


# route to find a goal with id that matches the goal_id of tasks
@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def send_list_of_tasks_ids_to_a_goal(goal_id):
    request_body = request.get_json()
    chosen_goal = validate_goal_id(goal_id)
    for task_id in request_body["task_ids"]:
        new_chosen_task = get_task_from_id(task_id)
        chosen_goal.tasks.append(new_chosen_task)

    db.session.commit()
    response_body = {
        "id": chosen_goal.goal_id,
        "task_ids": request_body["task_ids"]
    }
    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_task_of_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    tasks = []
    for item in goal.tasks:
        tasks.append(Task.to_dict(item))
    response_body = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks
    }
    db.session.commit()
    return jsonify(response_body), 200
