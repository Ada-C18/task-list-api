from flask import Blueprint, request, make_response, jsonify, abort
from app.models.goal import Goal
from app.models.task import Task
from app import db


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal) # track this object
    db.session.commit() # any changes that are pending commit those changes as data written in SQL

    new_goal_response = {"goal": new_goal.to_dict()}
    return make_response(jsonify(new_goal_response), 201)


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_list = [goal.to_dict() for goal in goals]
    return make_response(jsonify(goals_list), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)
    current_goal_response = {"goal": goal.to_dict()}

    return make_response(jsonify(current_goal_response), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    current_goal_response = {"goal": goal.to_dict()}
    return make_response(jsonify(current_goal_response), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def sending_list_of_task_ids_to_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    goal.tasks = [Task.query.get(task_id) for task_id in task_ids]
    
    db.session.commit() # any changes that are pending commit those changes as data written in SQL

    return make_response(jsonify({
            "id": goal.goal_id,
            "task_ids": task_ids
    }), 200)


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def getting_list_of_tasks_by_goal(goal_id):
    goal = get_validate_model(Goal, goal_id)

    tasks_list = [task.to_dict() for task in goal.tasks]

    return make_response(jsonify({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_list
        }), 200)

