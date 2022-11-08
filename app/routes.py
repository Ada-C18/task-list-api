from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app.models.goal import Goal
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details":"Invalid data"}, 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not "title" in request_body:
        return make_response({"details":"Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    sort_func = getattr(Task.title, sort_param)() if sort_param in ("asc", "desc") else None
    all_tasks = Task.query.order_by(sort_func).all()

    return jsonify([task.to_dict() for task in all_tasks])


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    all_goals = Goal.query.all()
    return jsonify([goal.to_dict() for goal in all_goals])


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()

    return {"task": task.to_dict()}


@goals_bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()

    return {"goal": goal.to_dict()}


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    validated_task = validate_model(Task, task_id)
    task = Task.query.get(validated_task.task_id)

    task.mark_complete()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    validated_task = validate_model(Task, task_id)
    task = Task.query.get(validated_task.task_id)

    task.mark_complete(False)
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}