from app import db
from .routes import validate_task
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return make_response({'goal': new_goal.to_dict()}, 201)


@goals_bp.route("", methods=["GET"])
def read_all_goals():

    title_query = request.args.get("title")
    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    else:
        goals = Goal.query.all()

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(goal_id)
    return {'goal': goal.to_dict()}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({'goal': goal.to_dict()}, 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()
    return make_response({f"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=['POST'])
def create_goals_of_task(goal_id):
    goal = validate_goal(goal_id)
    goal_tasks = []
    create_data = request.get_json()

    for task_id in create_data['task_ids']:
        task = validate_task(task_id)
        goal_tasks.append(task)

    goal_tasks = Goal(tasks=create_data["task_ids"])

    # response_task_ids = []

    # goal.tasks.append(task)
    # response_task_ids.append(task)
    # response_task_ids.append(task.task_id)

    db.session.add(goal_tasks)
    db.session.commit()

    # response_task_ids = []
    # for task in goal.tasks:
    #     response_task_ids.append(task.task_id)

    return make_response({
        "id": goal.goal_id,
        "task_ids": goal_tasks
    }, 201)
