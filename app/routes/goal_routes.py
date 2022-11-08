from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc


bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# CREATE
@bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response(jsonify({
            "details": "Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


# READ ALL
@bp.route("", methods=["GET"], strict_slashes=False)
def read_all_goals():
    sort_query = request.args.get("sort")

    goal_query = Goal.query

    if sort_query == "asc":
        goal_query = goal_query.order_by(asc(Goal.title))
    if sort_query == "desc":
        goal_query = goal_query.order_by(desc(Goal.title))

    goals = goal_query.all()
    response_body = [goal.to_dict() for goal in goals]

    return make_response(jsonify(response_body), 200)


# READ ONE
@bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

# UPDATE ALL ONE


@bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 200

# DELETE ONE TASK


@bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}),
        200)

# GOALS AND TASKS
# Sending a List of Task IDs to a Goal

@bp.route("/<goal_id>/tasks", methods=["POST"], strict_slashes=False)
def send_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks = []

    for task in request_body["task_ids"]:
        valid_task = validate_model(Task, task)
        tasks.append(valid_task)
        valid_task.goal = goal

    db.session.add(tasks)
    db.session.commit()

    return make_response(jsonify({"id": {goal.goal_id}, "task_ids": {goal.tasks}}), 200)


# GOALS AND TASKS
# Getting Tasks of One Goal
# Getting Tasks of One Goal: No Matching Tasks
# Getting Tasks of One Goal: No Matching Goal


@bp.route("/<goal_id>/tasks", methods=["GET"], strict_slashes=False)
def get_tasks_from_goal(goal_id):
    pass
    # goal = validate_model(Goal, goal_id)

    # tasks_response = []
    # for task in goal.tasks:
    #     tasks_response.append(task.to_dict())

    # return make_response(jsonify(goal.to_dict()))
