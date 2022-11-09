from app import db
from app.models.goal import Goal
from app.models.task import Task
from app.task_routes import validate_model, add_goal_to_task
from flask import abort, Blueprint, jsonify, make_response, redirect, request, url_for

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def post_a_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    return jsonify({"goal": new_goal.to_dict()}), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id, "get")
    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_task(goal_id):
    goal_to_update = validate_model(Goal, goal_id, "update")
    request_body = request.get_json()

    if request_body["title"]:
        goal_to_update.title = request_body["title"]

    db.session.commit()
    return jsonify({"goal": goal_to_update.to_dict()}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_task(goal_id):
    goal_to_delete = validate_model(Goal, goal_id, "delete")

    db.session.delete(goal_to_delete)
    db.session.commit()
    return jsonify({"details": f"Goal {goal_to_delete.goal_id} \"{goal_to_delete.title}\" successfully deleted"}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def update_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id, "get")
    response_body = request.get_json()
    for task_id in response_body["task_ids"]:
        task_to_update = validate_model(Task, task_id, "update")
        task_to_update.goal = goal
        db.session.commit()
        # redirect(url_for("tasks_bp.add_goal_to_task", task_id=id, json={"goal":goal.goal_id}))

    return jsonify({
        "id": goal.goal_id,
        "task_ids": response_body["task_ids"]}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_model(Goal, goal_id, "get")
    if goal.tasks:
        return jsonify(goal.to_dict()), 200
    else:
        return jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": []
        }), 200