from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal


task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


@task_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"], description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201


@goal_bp.route("", methods=["POST"])
def post_goal():
    request_body = request.get_json()
    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()
    return {"goal": new_goal.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort = request.args.get("sort")
    sort = getattr(Task.title, sort)() if sort in ("asc", "desc") else None
    return jsonify([t.to_dict() for t in Task.query.order_by(sort).all()])


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    return jsonify([g.to_dict() for g in Goal.query.all()])


@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return {"task": task.to_dict()}


@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return {"goal": goal.to_dict()}


@task_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    form_data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.title = form_data["title"]
    task.description = form_data["description"]
    db.session.commit()
    return {"task": task.to_dict()}


@goal_bp.route("/<goal_id>", methods=["PUT"])
def put_goal(goal_id):
    form_data = request.get_json()
    goal = Goal.query.get_or_404(goal_id)
    goal.title = form_data["title"]
    db.session.commit()
    return {"goal": goal.to_dict()}


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}


@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    db.session.delete(goal)
    db.session.commit()
    return {"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete()
    db.session.commit()
    return {"task": task.to_dict()}


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete(False)
    db.session.commit()
    return {"task": task.to_dict()}


from psycopg2.errors import InvalidTextRepresentation


@task_bp.errorhandler(404)
def handle_task_not_found(e):
    return {"details": "Task not found"}, 404


@goal_bp.errorhandler(404)
def handle_goal_not_found(e):
    return {"details": "Goal not found"}, 404


@task_bp.errorhandler(InvalidTextRepresentation)
def handle_task_invalid_id(e):
    return {"details": "Task id must be numeric"}, 400


@task_bp.errorhandler(KeyError)
def task_handle_invalid_data(e):
    return {"details": "Invalid data"}, 400


@goal_bp.errorhandler(KeyError)
def goal_handle_invalid_data(e):
    return {"details": "Invalid data"}, 400
