from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.helper_validate import validate_model

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# read all tasks
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

# read one task
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}

# # create new task
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except:
        return abort(make_response({"details": 'Invalid data'}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

# update task
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return {"goal": goal.to_dict()}

# delete task
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)

# nested route
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_id_list = request_body["task_ids"]

    for id in task_id_list:
        task = validate_model(Task, id)
        task.goal = goal
        db.session.add(task)
        db.session.commit()

    return {
        "id": goal.goal_id,
        "task_ids": task_id_list
    }

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = [task.to_dict() for task in goal.tasks]

    tasks_response = {
        "id": goal.goal_id,
        "title": goal.title,
        "tasks": tasks
        }
    return jsonify(tasks_response)