from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import datetime
from app.models.goal import Goal

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def get_one_model_or_error(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response_body = "Invalid data"
        abort(make_response(jsonify({"details": response_body}), 400))

    selected_obj = cls.query.get(model_id)

    if selected_obj is None:
        response_body = "Not found"
        abort(make_response(jsonify({"message": response_body}), 404))

    return selected_obj

@tasks_bp.route("", methods=["POST"])
def add_task():

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = Task.to_dict(new_task)

    return jsonify({"task": response}), 201 


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_params = request.args.get("sort")

    tasks = Task.query.all()

    response = []

    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        response.append(task_dict)

    if sort_params == "asc":
        response = sorted(response, key=lambda task: task['title'])
    elif sort_params == "desc":
        response = sorted(response, key=lambda task: task['title'], reverse=True)
    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_model_or_error(Task, task_id)

    response = Task.to_dict(chosen_task)

    return jsonify({"task": response}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_title_and_description(task_id):
    task_to_update = get_one_model_or_error(Task, task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    response_body = Task.to_dict(task_to_update)

    return jsonify({"task": response_body}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_data_from_db(task_id):

    task_to_delete = get_one_model_or_error(Task, task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    response_body = f'Task {task_id} "{task_to_delete.title}" successfully deleted'
    return jsonify({"details": response_body}), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task_to_complete = get_one_model_or_error(Task, task_id)

    task_to_complete.completed_at = datetime.today()
    
    db.session.add(task_to_complete)
    db.session.commit()
    
    return jsonify({"task": task_to_complete.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    incomplete_task = get_one_model_or_error(Task, task_id)

    incomplete_task.completed_at = None

    db.session.add(incomplete_task)
    db.session.commit()

    return jsonify({"task": incomplete_task.to_dict()}), 200


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def add_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": Goal.to_dict(new_goal)}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response = []

    for goal in goals:
        response.append(Goal.to_dict(goal))
    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = get_one_model_or_error(Goal, goal_id)

    response = Goal.to_dict(chosen_goal)

    return jsonify({"goal": response}), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal_title(goal_id):
    goal_to_update = get_one_model_or_error(Goal, goal_id)

    request_body = request.get_json()

    goal_to_update.title = request_body["title"]

    db.session.commit()

    response_body = Goal.to_dict(goal_to_update)

    return jsonify({"goal": response_body}), 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_data_from_db(goal_id):

    goal_to_delete = get_one_model_or_error(Goal, goal_id)

    db.session.delete(goal_to_delete)
    db.session.commit()

    response_body = f'Goal {goal_id} "{goal_to_delete.title}" successfully deleted'
    return jsonify({"details": response_body}), 200


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_list_of_tasks_to_goal(goal_id):

    valid_goal = get_one_model_or_error(Goal, goal_id)

    request_body = request.get_json()

    for task in request_body["task_ids"]:
        current_task = get_one_model_or_error(Task, task)
        current_task.goals = valid_goal

        db.session.commit()

    task_id_list = [task.task_id for task in valid_goal.tasks]

    response_body = {
        "id": valid_goal.goal_id,
        "task_ids": task_id_list
    }

    return jsonify(response_body), 200


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_of_one_goal(goal_id):
    valid_goal = get_one_model_or_error(Goal, goal_id)

    list_of_tasks = []

    for task in valid_goal.tasks:
        list_of_tasks.append(Task.to_dict(task))
    
    goal_dict = {
        "id": valid_goal.goal_id,
        "title": valid_goal.title,
        "tasks" : list_of_tasks
    }

    return jsonify(goal_dict), 200