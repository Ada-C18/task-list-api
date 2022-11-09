from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.goal import Goal


task_bp = Blueprint("task", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# ======
# Routes
# ======


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
    by = request.args.get("by")
    by = getattr(Task, by) if by in ("title", "task_id") else Task.title
    sort = request.args.get("sort")
    order_by = getattr(by, sort)() if sort in ("asc", "desc") else None

    title = request.args.get("title")
    filter = Task.title.like(f"%{title}%") if title else None

    query = Task.query
    query = query.filter(filter) if title else query
    query = query.order_by(order_by) if sort else query

    return jsonify([t.to_dict() for t in query.all()])


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    sort = request.args.get("sort")
    sort = getattr(Goal.title, sort)() if sort in ("asc", "desc") else None
    return jsonify([g.to_dict() for g in Goal.query.order_by(sort).all()])


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
    task.update(**form_data)
    db.session.commit()
    return {"task": task.to_dict()}


@goal_bp.route("/<goal_id>", methods=["PUT"])
def put_goal(goal_id):
    form_data = request.get_json()
    goal = Goal.query.get_or_404(goal_id)
    goal.update(**form_data)
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


@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    request_body = request.get_json()
    goal.add_tasks(request_body["task_ids"])
    db.session.commit()
    return {"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}, 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return goal.to_dict(tasks=True), 200


# ==============
# Error Handlers
# ==============


@task_bp.errorhandler(404)
def handle_task_not_found(e):
    return {"details": "Task not found"}, 404


@goal_bp.errorhandler(404)
def handle_goal_not_found(e):
    return {"details": "Goal not found"}, 404


@task_bp.errorhandler(KeyError)
@goal_bp.errorhandler(KeyError)
def handle_invalid_data(e):
    return {"details": "Invalid data"}, 400


@task_bp.errorhandler(ValueError)
@goal_bp.errorhandler(ValueError)
def handle_invalid_data(e):
    return {"details": str(e)}, 400


from psycopg2.errors import InvalidTextRepresentation


@task_bp.errorhandler(InvalidTextRepresentation)
@goal_bp.errorhandler(InvalidTextRepresentation)
def handle_goal_invalid_id(e):
    return {"details": str(e)}, 400
